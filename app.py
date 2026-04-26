from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# CREATE TABLE + AUTO DATA
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

    count = conn.execute('SELECT COUNT(*) FROM properties').fetchone()[0]

    if count == 0:
        properties = [
            ("1BHK Flat", "Pune", 12000), ("2BHK Apartment", "Mumbai", 25000),
            ("3BHK Luxury Flat", "Bangalore", 45000), ("Studio Apartment", "Delhi", 10000),
            ("1RK Room", "Chennai", 8000), ("2BHK Flat", "Hyderabad", 20000),
            ("3BHK Villa", "Goa", 50000), ("1BHK Furnished", "Pune", 15000),
            ("2BHK Semi-Furnished", "Mumbai", 22000), ("Luxury Penthouse", "Delhi", 80000),
            ("1BHK Flat", "Noida", 11000), ("2BHK Apartment", "Gurgaon", 23000),
            ("3BHK Flat", "Kolkata", 30000), ("Studio Flat", "Indore", 9000),
            ("1RK Room", "Nagpur", 7000), ("2BHK Flat", "Surat", 18000),
            ("3BHK Villa", "Jaipur", 40000), ("1BHK Furnished", "Lucknow", 12000),
            ("2BHK Semi-Furnished", "Bhopal", 17000), ("Luxury Flat", "Chandigarh", 35000),
            ("1BHK Flat", "Pune", 13000), ("2BHK Apartment", "Mumbai", 26000),
            ("3BHK Luxury Flat", "Bangalore", 47000), ("Studio Apartment", "Delhi", 11000),
            ("1RK Room", "Chennai", 8500), ("2BHK Flat", "Hyderabad", 21000),
            ("3BHK Villa", "Goa", 52000), ("1BHK Furnished", "Pune", 15500),
            ("2BHK Semi-Furnished", "Mumbai", 24000), ("Luxury Penthouse", "Delhi", 85000),
            ("1BHK Flat", "Noida", 11500), ("2BHK Apartment", "Gurgaon", 25000),
            ("3BHK Flat", "Kolkata", 32000), ("Studio Flat", "Indore", 9500),
            ("1RK Room", "Nagpur", 7500), ("2BHK Flat", "Surat", 19000),
            ("3BHK Villa", "Jaipur", 42000), ("1BHK Furnished", "Lucknow", 13000),
            ("2BHK Semi-Furnished", "Bhopal", 18000), ("Luxury Flat", "Chandigarh", 37000),
            ("1BHK Flat", "Pune", 14000), ("2BHK Apartment", "Mumbai", 27000),
            ("3BHK Luxury Flat", "Bangalore", 48000), ("Studio Apartment", "Delhi", 12000),
            ("1RK Room", "Chennai", 9000), ("2BHK Flat", "Hyderabad", 22000),
            ("3BHK Villa", "Goa", 55000), ("1BHK Furnished", "Pune", 16000),
            ("2BHK Semi-Furnished", "Mumbai", 26000), ("Luxury Penthouse", "Delhi", 90000)
        ]

        conn.executemany(
            'INSERT INTO properties (title, location, price) VALUES (?, ?, ?)',
            properties
        )

    conn.commit()
    conn.close()

create_table()


# -----------------------------
# ROUTES
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


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


@app.route('/properties')
def view_properties():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties').fetchall()
    conn.close()
    return render_template('properties.html', properties=properties)


@app.route('/property/<int:id>')
def property_detail(id):
    conn = get_db_connection()
    property = conn.execute(
        'SELECT * FROM properties WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    return render_template('property_detail.html', property=property)


if __name__ == '__main__':
    app.run(debug=True)
