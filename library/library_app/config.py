"File with consts for library_app."
from os.path import join


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

SAFE_METHODS = 'GET', 'HEAD', 'OPTIONS'
UNSAFE_METHODS = 'POST', 'PUT', 'DELETE'

CHARS_DEFAULT = 40