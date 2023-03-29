from django.contrib import admin
from datetime import datetime
from .models import Genre, Book, Author, BookAuthor, BookGenre


DECADE = 10


class NewestBookListFilter(admin.SimpleListFilter):

    title = 'recency'
    parameter_name = 'recency'

    def lookups(self, *_):
        return (
            ('10yo', 'Written in the last 10 years'),
            ('20yo', 'Written in the last 20 years'),
        )

    def queryset(self, _, queryset):
        if self.value() == '10yo':
            return queryset.filter(year__gte=datetime.now().year - DECADE)
        elif self.value() == '20yo':
            return queryset.filter(year__gte=datetime.now().year - DECADE * 2)
        return queryset


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Register Genre Admin Model."""

    model = Genre
    list_filter = (
        'name',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Register Book Admin Model."""

    model = Book
    inlines = (BookAuthorInline, BookGenreInline)
    list_filter = (
        'type',
        'genres',
        NewestBookListFilter,
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Register Author Admin Model."""

    model = Author
    inlines = (BookAuthorInline,)
    list_filter = (
        'full_name',
    )
