from django.shortcuts import render
from .models import Book, Genre, Author
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer
from rest_framework.permissions import BasePermission
from . import config


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


def catalog_view(cls_model, context_name, template):
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


class Permission(BasePermission):
    def has_permission(self, request, _):
        if request.method in config.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in config.UNSAFE_METHODS:
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewset(cls_model, serializer, order_field):
    class CustomViewSet(ModelViewSet):
        serializer_class = serializer
        queryset = cls_model.objects.all().order_by(order_field)
        permission_classes = [Permission]

        def get_queryset(self):
            objects = cls_model.objects.all()
            query = {}
            for param in serializer.Meta.fields:
                value = self.request.GET.get(param, '')
                if value:
                    query[param] = value
            if query:
                objects = objects.filter(**query)
            return objects.order_by(order_field)

    return CustomViewSet


BookViewSet = create_viewset(Book, BookSerializer, 'title')
AuthorViewSet = create_viewset(Author, AuthorSerializer, 'full_name')
GenreViewSet = create_viewset(Genre, GenreSerializer, 'name')
