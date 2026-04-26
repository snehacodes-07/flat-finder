from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# SQLite connection
db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    location TEXT,
    price INTEGER
)
""")
db.commit()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Add Property
@app.route('/add', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        price = request.form['price']

        query = "INSERT INTO properties (title, location, price) VALUES (?, ?, ?)"
        values = (title, location, price)

        cursor.execute(query, values)
        db.commit()

        return "Property Added!"

    return render_template('add_property.html')


# View Properties
@app.route('/properties')
def view_properties():
    cursor.execute("SELECT * FROM properties")
    data = cursor.fetchall()
    return render_template('properties.html', properties=data)


# Property Detail Page
@app.route('/property/<int:id>')
def property_detail(id):
    query = "SELECT * FROM properties WHERE id = ?"
    cursor.execute(query, (id,))
    data = cursor.fetchone()

    return render_template('property_detail.html', property=data)


# Run App
if __name__ == '__main__':
    app.run(debug=True)
