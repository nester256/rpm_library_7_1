from django.db import models
from django.core.exceptions import ValidationError
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True

class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), blank=True, null=True)

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), blank=True, null=True)

    class Meta:
        abstract = True


class Author(UUIDMixin, CreatedMixin, ModifiedMixin):
    full_name = models.TextField(_('full name'))
    books = models.ManyToManyField('Book', verbose_name=_('books'), through='BookAuthor')

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'author'
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        

def validate_volume(volume: int):
    if volume <= 0:
        raise ValidationError(   # from django.core.exceptions
            f'Volume {volume} is less or equal zero',
            params={'volume': volume}
        )

# types of goods
type_choices = (
    ('book', _('book')),
    ('magazine', _('magazine'))
)

class Book(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.CharField(_('title'), max_length=40)
    description = models.TextField(_('description'), blank=True, null=True)
    volume = models.IntegerField(_('volume'), validators=[validate_volume])
    type = models.CharField(_('type'), max_length=20, choices=type_choices, blank=True, null=True)
    year = models.IntegerField(_('year'), blank=True, null=True)
    authors = models.ManyToManyField(Author, verbose_name=_('authors'), through='BookAuthor')
    genres = models.ManyToManyField('Genre', verbose_name=_('genres'), through='BookGenre')

    def __str__(self):
        return f'{self.title}, {self.type}, {self.year}.'

    class Meta:
        db_table = 'book'
        verbose_name = _('book')
        verbose_name_plural = _('books')


class BookAuthor(UUIDMixin, CreatedMixin):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'book_author'
        unique_together = (('book', 'author'),)


genre_choices = (
    ('fantasy', _('fantasy')),
    ('fiction', _('fiction')),
    ('detective', _('detective'))
)

class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.CharField(_('name'), choices=genre_choices, max_length=30)
    description = models.TextField(_('description'), blank=True, null=True)
    books = models.ManyToManyField(Book, verbose_name=_('books'), through='BookGenre')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class BookGenre(UUIDMixin, CreatedMixin):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'book_genre'
        unique_together = (('book', 'genre'),)



