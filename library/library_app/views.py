from django.shortcuts import render
from .models import Book, Genre, Author
from django.views.generic import ListView
from django.core.paginator import Paginator
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer
from . import config
from rest_framework import status as status_codes
from rest_framework import decorators, permissions, viewsets, parsers
from rest_framework.response import Response
from django.db.models import Model
from .weather import get_weather
from .forms import WeatherForm


@decorators.api_view(['GET'])
def weather_rest(request):
    query = query_from_request(request)
    location = query.get('location')
    if not location or location not in config.LOCATIONS_COORDINATES.keys():
        return Response(
            'Wrong query value for <location>',
            status=status_codes.HTTP_400_BAD_REQUEST
        )
    response = get_weather(location)
    if not response or response.status_code != status_codes.HTTP_200_OK:
        return Response(
            'Foreign API did not respond',
            status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(
        response.json().get('fact'),
        status=status_codes.HTTP_200_OK
    )


def weather_page(request):
    query = query_from_request(request)
    print(f'weather page got query: {query}')
    location = query.get('location')
    if not location:
        weather_data = {}
    else:
        response = get_weather(location)
        if not response or response.status_code != status_codes.HTTP_200_OK:
            weather_data = {}
        else:
            weather_data = response.json().get('fact')

    return render(
        request,
        config.TEMPLATE_WEATHER,
        context={
            'form': WeatherForm(),
            'weather_data': weather_data
        }
    )


def custom_main(req):
    return render(
        req,
        config.TEMPLATE_MAIN,
        context={
            'books': Book.objects.all().count(),
            'authors': Author.objects.all().count(),
            'genres': Genre.objects.all().count(),
        }
    )


def catalog_view(cls_model: Model, context_name, template):
    class CustomListView(ListView):
        model = cls_model
        template_name = template
        paginate_by = config.PAGINATE_THRESHOLD
        context_object_name = context_name

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            objects = cls_model.objects.all()
            paginator = Paginator(objects, config.PAGINATE_THRESHOLD)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{context_name}_list'] = page_obj
            return context
    return CustomListView


def entity_view(cls_model, name, template):
    def view(req):
        return render(
            req,
            template,
            context={
                name: cls_model.objects.get(id=req.GET.get('id', ''))
            }
        )
    return view


BookListView = catalog_view(Book, 'books', config.BOOKS_CATALOG)
book_view = entity_view(Book, 'book', config.BOOK_ENTITY)

AuthorListView = catalog_view(Author, 'authors', config.AUTHORS_CATALOG)
author_view = entity_view(Author, 'author', config.AUTHOR_ENTITY)

GenreListView = catalog_view(Genre, 'genres', config.GENRES_CATALOG)
genre_view = entity_view(Genre, 'genre', config.GENRE_ENTITY)


class Permission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in config.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in config.UNSAFE_METHODS:
            return bool(request.user and request.user.is_superuser)
        return False


def query_from_request(request, cls_serializer=None) -> dict:
    if cls_serializer:
        query = {}
        for param in cls_serializer.Meta.fields:
            value = request.GET.get(param, '')
            if value:
                query[param] = value
        return query
    return request.GET


def create_viewset(cls_model: Model, serializer, order_field):
    class CustomViewSet(viewsets.ModelViewSet):
        serializer_class = serializer
        queryset = cls_model.objects.all().order_by(order_field)
        permission_classes = [Permission]

        def get_queryset(self):
            objects = cls_model.objects.all()
            query = query_from_request(self.request, serializer)
            if query:
                objects = objects.filter(**query)
            return objects.order_by(order_field)

        def delete(self, request):
            query = query_from_request(request, serializer)
            if query:
                objects = cls_model.objects.filter(**query)
                objects_num = len(objects)
                if not objects_num:
                    content = f'DELETE query {query} did not match any instances of {cls_model.__name__}'
                    return Response(content, status=status_codes.HTTP_404_NOT_FOUND)
                try:
                    objects.delete()
                except Exception as error:
                    return Response(error, status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
                content = f'DELETED {objects_num} instances of {cls_model.__name__}'
                status = status_codes.HTTP_204_NO_CONTENT if objects_num == 1 else status_codes.HTTP_200_OK
                return Response(content, status=status)
            return Response('DELETE has got no query', status=status_codes.HTTP_400_BAD_REQUEST)

        def put(self, request):
            def serialize(target):
                content = parsers.JSONParser().parse(request)
                if target:
                    serialized = serializer(target, data=content, partial=True)
                    status = status_codes.HTTP_200_OK
                    body = f'PUT has updated instance of {cls_model.__name__} id={target.id}'
                else:
                    serialized = serializer(data=content, partial=True)
                    status = status_codes.HTTP_201_CREATED
                    body = f'PUT has created a new instance of {cls_model.__name__}'

                if not serialized.is_valid():
                    return status_codes.HTTP_400_BAD_REQUEST, f'PUT could not process content: {content}'

                try:
                    serialized.save()
                except Exception as error:
                    return status_codes.HTTP_500_INTERNAL_SERVER_ERROR, error
                return status, body

            query = query_from_request(request, serializer)
            target_id = query.get('id', '')
            if target_id:
                target_object = cls_model.objects.get(id=target_id)
                status, body = serialize(target_object)
                return Response(body, status=status)
            return Response('PUT has got no id primary key', status=status_codes.HTTP_400_BAD_REQUEST)

    return CustomViewSet


BookViewSet = create_viewset(Book, BookSerializer, 'title')
AuthorViewSet = create_viewset(Author, AuthorSerializer, 'full_name')
GenreViewSet = create_viewset(Genre, GenreSerializer, 'name')
