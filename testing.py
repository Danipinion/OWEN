import requests
import random
import time

# Ganti dengan IP dan port Flask Anda jika berbeda
FLASK_URL = "http://127.0.0.1:5000/upload"  # Pastikan ini benar

def generate_random_data():
    """Menghasilkan data sensor acak."""
    data = {
        "suhu": round(random.uniform(20, 35), 2),
        "kelembaban": round(random.uniform(50, 80), 2),
        "tegangan": round(random.uniform(10, 14), 2),
        "turbidity": round(random.uniform(0, 100), 2),
        "ph": round(random.uniform(6, 8), 2),
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return data

def send_data(url, data):
    """Mengirim data ke server Flask."""
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Data dikirim. Status kode: {response.status_code}")
        print(f"Respon server: {response.text}")  # Cetak respon dari server
    except requests.exceptions.RequestException as e:
        print(f"Error mengirim data: {e}")

if __name__ == "__main__":
    print(f"Mengirim data ke {FLASK_URL} setiap 10 detik...")
    try:
        while True:
            random_data = generate_random_data()
            print("Data yang dihasilkan:", random_data)
            send_data(FLASK_URL, random_data)
            time.sleep(10)
    except KeyboardInterrupt:
        print("Pengiriman data dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
