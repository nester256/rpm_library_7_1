"""library_app URL Configuration"""
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# register our REST views in router object
router.register(r'Book', views.BookViewSet)
router.register(r'Genre', views.GenreViewSet)
router.register(r'Author', views.AuthorViewSet)

urlpatterns = [
    path('homepage/', views.custom_main, name='homepage'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('book/', views.book_view, name='book'),
    path('genre/', views.genre_view, name='genre'),
    path('author/', views.author_view, name='author'),
    # REST
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
