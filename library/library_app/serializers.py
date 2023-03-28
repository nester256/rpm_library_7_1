from .models import Book, Genre, Author
from rest_framework.serializers import HyperlinkedModelSerializer


class BookSerializer(HyperlinkedModelSerializer):
    model = Book
    fields = ('title', 'description', 'type', 'volume', 'year', 'created', 'modified')

class AuthorSerializer(HyperlinkedModelSerializer):
    model = Author
    fields = ('full_name',) # tuple

class GenreSerializer(HyperlinkedModelSerializer):
    model = Genre
    fields = ('name', 'description')