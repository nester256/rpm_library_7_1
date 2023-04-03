"File with consts for library_app."
from os.path import join
from dotenv import load_dotenv
from os import getenv


TEMPLATE_MAIN = 'index.html'
TEMPLATE_WEATHER = 'pages/weather.html'
CATALOG = 'catalog'
BOOKS_CATALOG = join(CATALOG, 'books.html')
AUTHORS_CATALOG = join(CATALOG, 'authors.html')
GENRES_CATALOG = join(CATALOG, 'genres.html')

ENTITIES = 'entities'
BOOK_ENTITY = join(ENTITIES, 'book.html')
AUTHOR_ENTITY = join(ENTITIES, 'author.html')
GENRE_ENTITY = join(ENTITIES, 'genre.html')

PAGINATE_THRESHOLD = 20

SAFE_METHODS = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
UNSAFE_METHODS = 'POST', 'PUT', 'DELETE'

CHARS_DEFAULT = 40

# weather consts
COLLEGE_LOCATION = {'lat': 43.403438, 'lon': 39.981544}
SOCHI_LOCATION = {'lat': 43.713351, 'lon': 39.580041}
POLYANA_LOCATION = {'lat': 43.661294, 'lon': 40.268936}
LOCATIONS_COORDINATES = {
    'college': COLLEGE_LOCATION,
    'sochi': SOCHI_LOCATION,
    'polyana': POLYANA_LOCATION
}
# location choices for WeatherForm
LOCATIONS_NAMES = [(key, key) for key in LOCATIONS_COORDINATES]

YANDEX_API_URL = 'https://api.weather.yandex.ru/v2/informers'
YANDEX_API_HEADER = 'X-Yandex-API-Key'
YANDEX_KEY = getenv('YANDEX_KEY')