from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize database
def init_db():
    if not os.path.exists('instance'):
        os.makedirs('instance')
    conn = sqlite3.connect('instance/healthtrack.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS activities (id INTEGER PRIMARY KEY, user_id INTEGER, activity TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('instance/healthtrack.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('instance/healthtrack.db')
        c = conn.cursor()
        c.execute("SELECT id, name, password FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('instance/healthtrack.db')
    c = conn.cursor()
    c.execute("SELECT activity, date FROM activities WHERE user_id = ? ORDER BY date DESC", (session['user_id'],))
    activities = c.fetchall()
    
    # Generate activity summary for the bar chart
    activity_summary = {}
    for activity, date in activities:
        activity_summary[activity] = activity_summary.get(activity, 0) + 1
    
    conn.close()
    return render_template('dashboard.html', activities=activities, activity_summary=activity_summary)

@app.route('/add', methods=['GET', 'POST'])
def add_activity():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        activity = request.form['activity']
        conn = sqlite3.connect('instance/healthtrack.db')
        c = conn.cursor()
        c.execute("INSERT INTO activities (user_id, activity) VALUES (?, ?)", (session['user_id'], activity))
        conn.commit()
        conn.close()
        flash('Activity added!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_activity.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
