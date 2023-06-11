from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Update the connection string with your Azure SQL Database details
CONNECTION_STRING = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:vot-books.database.windows.net,1433;Database=books;Uid=yana;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def create_table():
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(255) NOT NULL,
            author NVARCHAR(255) NOT NULL,
            genre NVARCHAR(255) NOT NULL,
            comment NVARCHAR(MAX)
        )
    ''')
    conn.commit()
    conn.close()

def get_all_books():
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return books

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        comment = request.form['comment']

        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, genre, comment)
            VALUES (?, ?, ?, ?)
        ''', (title, author, genre, comment))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/read_books')
def read_books():
    search_query = request.args.get('search_query', '')

    # Connect to Azure SQL Database
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    if search_query:
        # Perform a search query using the provided search query
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR genre LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        # Retrieve all books from the database
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()
    conn.close()

    return render_template('read_books.html', books=books, search_query=search_query)


@app.route('/clean_database')
def clean_database():
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books")
    conn.commit()
    conn.close()
    return redirect(url_for('read_books'))

if __name__ == '__main__':
    create_table()
    app.run(port=8080)
