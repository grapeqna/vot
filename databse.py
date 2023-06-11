import sqlite3
from elasticsearch import Elasticsearch

conn = sqlite3.connect('book_diary.db')

conn.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        comment TEXT
    )
''')
conn.commit()

es = Elasticsearch(['localhost:9200'])

def add_book(title, author, genre, comment):
    conn.execute('''
        INSERT INTO books (title, author, genre, comment)
        VALUES (?, ?, ?, ?)
    ''', (title, author, genre, comment))
    conn.commit()

    es.index(index='books', body={
        'title': title,
        'author': author,
        'genre': genre,
        'comment': comment
    })

def get_all_books():
    cursor = conn.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return books

def search_books(query):
    es_results = es.search(index='books', body={
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title', 'author', 'genre', 'comment']
            }
        }
    })

    hits = es_results['hits']['hits']
    books = [hit['_source'] for hit in hits]
    return books

