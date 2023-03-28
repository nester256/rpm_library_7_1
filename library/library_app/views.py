from django.shortcuts import render
from .models import Book, Genre, Author
from django.views.generic import ListView
from django.core.paginator import Paginator
from os.path import join
from rest_framework.viewsets import ModelViewSet
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer


TEMPLATE_MAIN = 'index.html'

CATALOG = 'catalog'
BOOKS_CATALOG = join(CATALOG, 'books.html')
AUTHORS_CATALOG = join(CATALOG, 'authors.html')
GENRES_CATALOG = join(CATALOG, 'genres.html')

ENTITIES = 'entities'
BOOK_ENTITY = join(ENTITIES, 'book.html')
AUTHOR_ENTITY = join(ENTITIES, 'author.html')
GENRE_ENTITY = join(ENTITIES, 'genre.html')

PAGINATE_THRESHOLD = 20

def custom_main(req):
    """This view shows the count of all main objects."""
    return render(
        req,
        TEMPLATE_MAIN, 
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
        paginate_by = PAGINATE_THRESHOLD
        context_object_name = context_name

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            objects = cls_model.objects.all()
            paginator = Paginator(objects, PAGINATE_THRESHOLD)
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

BookListView = catalog_view(Book, 'books', BOOKS_CATALOG)
book_view = entity_view(Book, 'book', BOOK_ENTITY)

AuthorListView = catalog_view(Author, 'authors', AUTHORS_CATALOG)
author_view = entity_view(Author, 'author', AUTHOR_ENTITY)

GenreListView = catalog_view(Genre, 'genres', GENRES_CATALOG)
genre_view = entity_view(Genre, 'genre', GENRE_ENTITY)


def create_viewset(cls_model, serializer, order_field):
    class CustomViewSet(ModelViewSet):
        serializer_class = serializer
        queryset = cls_model.objects.all().order_by(order_field)

        def get_queryset(self):
                query = {}
                for param in serializer.Meta.fields:
                    value = self.request.GET.get(param, '')
                    if value:
                        query[param] = value
                    
                objects = cls_model.objects.all().filter(**query) if id else cls_model.objects.all()
                return objects.order_by(order_field)

    return CustomViewSet

BookViewSet = create_viewset(Book, BookSerializer, 'title')
AuthorViewSet = create_viewset(Author, AuthorSerializer, 'full_name')
GenreViewSet = create_viewset(Genre, GenreSerializer, 'name')
