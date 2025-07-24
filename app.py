from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT,
            brand TEXT
        )
    ''')
    conn.close()


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        brand = request.form['brand']

        conn = sqlite3.connect('users.db')
        conn.execute(
            'INSERT INTO users (name, email, address, brand) VALUES (?, ?, ?, ?)',
            (name, email, address, brand)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('register'))  

    return render_template('register.html')


@app.route('/users')
def view_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)


@app.route('/logout')
def logout():
    return """
    <h2 style='text-align:center; color:gold; background:#000; padding:20px;'>You have been logged out.</h2>
    <div style='text-align:center; margin-top:20px;'>
        <a href='/register' style='color:#FFD700; font-weight:bold;'>← Back to Register</a>
    </div>
    """


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
