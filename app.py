from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS USERS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO USERS(USERNAME, PASSWORD) VALUES(?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM USERS WHERE USERNAME=? AND PASSWORD=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            return "Login Successful!"
        else:
            return "Invalid Username Or Password"

    return render_template("login.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)