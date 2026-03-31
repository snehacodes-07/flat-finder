from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="flat_finder"
)

cursor = db.cursor()

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

        query = "INSERT INTO properties (title, location, price) VALUES (%s, %s, %s)"
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
    query = "SELECT * FROM properties WHERE id = %s"
    cursor.execute(query, (id,))
    data = cursor.fetchone()

    return render_template('property_detail.html', property=data)


# Run App
if __name__ == '__main__':
    app.run(debug=True)