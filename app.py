from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row   # allows column access by name
    return conn


# -----------------------------
# CREATE TABLE (FIRST TIME ONLY)
# -----------------------------
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -----------------------------
# ADD PROPERTY
# -----------------------------
@app.route('/add', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        price = request.form['price']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO properties (title, location, price) VALUES (?, ?, ?)',
            (title, location, price)
        )
        conn.commit()
        conn.close()

        return redirect('/properties')

    return render_template('add_property.html')


# -----------------------------
# VIEW ALL PROPERTIES
# -----------------------------
@app.route('/properties')
def view_properties():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties').fetchall()
    conn.close()

    return render_template('properties.html', properties=properties)


# -----------------------------
# PROPERTY DETAILS
# -----------------------------
@app.route('/property/<int:id>')
def property_detail(id):
    conn = get_db_connection()
    property = conn.execute(
        'SELECT * FROM properties WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    return render_template('property_detail.html', property=property)


# -----------------------------
# RUN APP
#----------------------------
if __name__ == '__main__':
    app.run(debug=True)
