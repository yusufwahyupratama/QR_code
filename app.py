import os
import time
import random
from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

# Pastikan folder 'static' ada
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Satu route saja:
    - GET  -> menampilkan form awal.
    - POST -> memproses pembuatan QR Code, menampilkan preview di halaman yang sama.
    """
    file_name = None  # Variabel untuk menampung nama file QR Code

    if request.method == 'POST':
        # Ambil data teks/URL dari form
        data = request.form.get('data', '')

        # Buat objek QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Generate gambar QR (hitam-putih)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Buat nama file unik (pakai timestamp + random)
        unique_suffix = f"{int(time.time())}_{random.randint(1000,9999)}"
        file_name = f"qrcode_{unique_suffix}.png"
        file_path = os.path.join('static', file_name)

        # Simpan QR Code
        qr_img.save(file_path)

    # Render template: jika file_name tidak None, berarti kita baru saja generate QR
    return render_template('index.html', file_name=file_name)

if __name__ == '__main__':
    # Jalankan server
    app.run(debug=True)
