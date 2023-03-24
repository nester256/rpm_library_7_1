from django.shortcuts import render
from .models import Book, Genre, Author


TEMPLATE_MAIN = 'index.html'

def custom_main(req):
    """This view shows the count of all main objects."""
    return render(
        req,
        TEMPLATE_MAIN, 
        context={
            'books': Book.objects.all().count(),
            'author': Author.objects.all().count(),
            'genres': Genre.objects.all().count(),
        }
    )