import pyodbc
from elasticsearch import Elasticsearch

# Update the connection details for Azure SQL Database
CONNECTION_STRING = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:vot-books.database.windows.net,1433;Database=books;Uid=yana;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Create a connection to Azure SQL Database
conn = pyodbc.connect(CONNECTION_STRING)

conn.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INT IDENTITY(1,1) PRIMARY KEY,
        title NVARCHAR(255) NOT NULL,
        author NVARCHAR(255) NOT NULL,
        genre NVARCHAR(255) NOT NULL,
        comment NVARCHAR(MAX)
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
