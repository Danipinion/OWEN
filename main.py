from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'owen_sic2025'

# File untuk menyimpan data (misalnya, data sensor dan lainnya)
DATA_FILE = 'data.txt'
USER_FILE = 'users.txt'  # File untuk menyimpan data pengguna

# Fungsi untuk memuat data dari file
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data

# Fungsi untuk menyimpan data ke file
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)  # Indentasi untuk keterbacaan

# Inisialisasi data (termasuk latest_data)
all_data = load_data(DATA_FILE)  # Load all data
if 'latest_data' not in all_data:
    all_data['latest_data'] = {
        "suhu": None,
        "kelembaban": None,
        "tegangan": None,
        "turbidity": None,
        "ph": None
    }
latest_data = all_data['latest_data'] #make latest_data global

def load_users():
    users_data = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 3:
                    username, password, nama = parts
                    users_data[username] = {'password': password, 'nama': nama}
                elif len(parts) == 2: #handle the case where nama is not provided
                    username,password = parts
                    users_data[username] = {'password': password, 'nama': ''} #set default nama
    return users_data

def save_user(username, password, nama=None):
    if nama is None:
        nama = ""  # Default value for nama
    with open(USER_FILE, 'a') as f:
        f.write(f'{username}:{password}:{nama}\n')

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('beranda'))  # Redirect ke beranda
    return redirect(url_for('login'))

@app.route('/beranda')
def beranda():
    if 'email' in session:
        return render_template('beranda.html', all_data=all_data)
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if 'email' in session:
        return render_template('menu.html')
    return redirect(url_for('login'))

@app.route('/notif')
def notif():
    if 'email' in session:
        return render_template('notif.html')
    return redirect(url_for('login'))

@app.route('/profil')
def profil():
    if 'email' in session:
        #  Ambil data pengguna dari file (misalnya nama) untuk ditampilkan di profil
        users = load_users()
        user_data = users.get(session['email'])
        return render_template('profile.html', user=user_data)
    return redirect(url_for('login'))

@app.route('/pasokan')
def pasokan():
    if 'email' in session:
        return render_template('pasokan.html')
    return redirect(url_for('login'))

@app.route('/kipas')
def kipas():
    if 'email' in session:
        return render_template('kipas.html')
    return redirect(url_for('login'))

@app.route('/pembuangan')
def pembuangan():
    if 'email' in session:
        return render_template('pembuangan.html')
    return redirect(url_for('login'))

@app.route('/sensor')
def sensor():
    if 'email' in session:
        return render_template('sensor.html')
    return redirect(url_for('login'))

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(latest_data)

@app.route('/upload', methods=['POST'])
def upload_data():
    global latest_data
    data = request.get_json()
    if data:
        print('Data diterima dari ESP32:', data)
        latest_data.update(data)
        all_data['latest_data'] = latest_data  # Update di all_data
        save_data(DATA_FILE, all_data)  # Simpan perubahan ke file
        return jsonify({'status': 'success', 'message': 'Data received'})
    return jsonify({'status': 'failed', 'message': 'No data received'}), 400

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users:
            return render_template('daftar.html', error='Email sudah terdaftar')
        save_user(email, password, nama)
        return redirect(url_for('login'))
    return render_template('daftar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users and users[email]['password'] == password:
            session['email'] = email
            return redirect(url_for('beranda'))  # Redirect ke beranda setelah login
        return render_template('login.html', error='Email atau password salah')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)