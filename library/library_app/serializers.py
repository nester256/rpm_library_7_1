from .models import Book, Genre, Author
from rest_framework.serializers import HyperlinkedModelSerializer


class BookSerializer(HyperlinkedModelSerializer):
        
    class Meta:
        model = Book
        fields = ('title', 'description', 'type', 'volume', 'year', 'created', 'modified')

class AuthorSerializer(HyperlinkedModelSerializer):
        
    class Meta:
        model = Author
        fields = ('full_name',)

class GenreSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name', 'description')