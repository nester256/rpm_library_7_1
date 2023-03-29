from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv
from random import choice


load_dotenv()
credentials = {
    'host': getenv('PG_HOST'),
    'port': int(getenv('PG_PORT')),
    'user': getenv('PG_USER'),
    'password': getenv('PG_PASSWORD'),
    'dbname': getenv('PG_DBNAME')
}

connection = connect(**credentials)
cursor = connection.cursor()

get_ids = 'select id from'
cursor.execute(f'{get_ids} library.book')
book_ids = [id_data[0] for id_data in cursor.fetchall()]

cursor.execute(f'{get_ids} library.genre')
genre_ids = [id_data[0] for id_data in cursor.fetchall()]

request = "INSERT INTO library.book_genre (book_id, genre_id) VALUES ('{0}', '{1}')"
iteration = 0
for book_id in book_ids:
    genre_id = choice(genre_ids)
    cursor.execute(request.format(book_id, genre_id))
    iteration += 1

connection.commit()
cursor.close()
connection.close()
