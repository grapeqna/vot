from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

DATABASE = 'book_diary.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_books():
    conn = sqlite3.connect(DATABASE)
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

        conn = sqlite3.connect(DATABASE)
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
    books = get_all_books()

    if search_query:
        books = [book for book in books if search_query.lower() in book[1].lower() or search_query.lower() in book[3].lower()]

    return render_template('read_books.html', books=books, search_query=search_query)

@app.route('/clean_database')
def clean_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books")
    conn.commit()
    conn.close()
    return redirect(url_for('read_books'))

if __name__ == '__main__':
    create_table()
    app.run(port=8080)
