from django.contrib import admin
from datetime import datetime
from .models import Genre, Book, Author, BookAuthor, BookGenre, genre_choices


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
            return queryset.filter(
                year__gte = datetime.now().year - 10
            )
        elif self.value() == '20yo':
            return queryset.filter(
                year__gte = datetime.now().year - 20
            )
        return queryset

class BookAuthor_inline(admin.TabularInline):
    model = BookAuthor
    extra = 1

class BookGenre_inline(admin.TabularInline):
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
    inlines = (BookAuthor_inline, BookGenre_inline)
    list_filter = (
        'type',
        'genres',
        NewestBookListFilter,
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Register Author Admin Model."""
    
    model = Author
    inlines = (BookAuthor_inline,)
    list_filter = (
        'full_name',
    )