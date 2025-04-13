from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# One-time DB creation function
def init_db():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            mobile TEXT,
            degree TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call the DB initializer
init_db()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    address = request.form['address']
    mobile = request.form['mobile']
    degree = request.form['degree']

    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("INSERT INTO person (name, address, mobile, degree) VALUES (?, ?, ?, ?)",
              (name, address, mobile, degree))
    conn.commit()
    conn.close()

    return redirect('/list')

@app.route('/list')
def list_people():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("SELECT * FROM person")
    data = c.fetchall()
    conn.close()
    return render_template('list.html', people=data)

if __name__ == '__main__':
    app.run(debug=True)
