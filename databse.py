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

# Create Elasticsearch client instance
es = Elasticsearch(['localhost:9200'])

# Function to add a book to the database
def add_book(title, author, genre, comment):
    conn.execute('''
        INSERT INTO books (title, author, genre, comment)
        VALUES (?, ?, ?, ?)
    ''', (title, author, genre, comment))
    conn.commit()

    # Index the book data in Elasticsearch
    es.index(index='books', body={
        'title': title,
        'author': author,
        'genre': genre,
        'comment': comment
    })

# Function to retrieve all books from the database
def get_all_books():
    cursor = conn.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return books

# Function to search books in Elasticsearch
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

# You can close the connection at an appropriate time in your application
# conn.close()
