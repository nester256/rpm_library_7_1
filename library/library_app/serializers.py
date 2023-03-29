from .models import Book, Genre, Author
from rest_framework.serializers import HyperlinkedModelSerializer


class BookSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'type', 'volume', 'year', 'created', 'modified')


class AuthorSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'full_name')


class GenreSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'description')
