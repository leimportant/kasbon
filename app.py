from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
# Data kasbon sementara, bisa digantikan dengan database
# Simulated in-memory database
kasbon_list = []
running_number = 1

# Route untuk halaman Home
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Route untuk menambah kasbon
@app.route('/add_kasbon', methods=['GET', 'POST'])
def add_kasbon():
    global running_number 
    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = request.form['jumlah']
        keterangan = request.form['keterangan']
        
        created_date = datetime.now()
        formatted_date = created_date.strftime("%Y%m%d")

        # Generate unique ID
        unique_id = f"{formatted_date}-{running_number}"
        # Menambahkan data kasbon ke dalam list
        kasbon_list.append({
            'id': unique_id, 
            'nama': nama,
            'jumlah': jumlah,
            'keterangan': keterangan,
            'created_date': created_date,
        })

        running_number += 1 
        return redirect(url_for('list_kasbon'))
    

    return render_template('kasbon/add_kasbon.html')

# Route untuk melihat daftar kasbon
@app.route('/list_kasbon')
def list_kasbon():
    return render_template('kasbon/list_kasbon.html', kasbons=kasbon_list)

@app.route('/edit_kasbon/<string:kasbon_id>', methods=['GET', 'POST'])
def edit_kasbon(kasbon_id):
    # Fetch the kasbon to edit
    kasbon = next((k for k in kasbon_list if k['id'] == kasbon_id), None)

    if kasbon is None:
        flash('Kasbon not found!', 'danger')
        return redirect(url_for('list_kasbon'))

    if request.method == 'POST':
        # Update kasbon data
        kasbon['nama'] = request.form['nama']
        kasbon['jumlah'] = request.form['jumlah']
        kasbon['keterangan'] = request.form['keterangan']
        flash('Kasbon updated successfully!', 'success')
        return redirect(url_for('list_kasbon'))

    return render_template('kasbon/edit_kasbon.html', kasbon=kasbon)

# Route untuk laporan kasbon
@app.route('/laporan_kasbon')
def laporan_kasbon():
    return render_template('kasbon/laporan_kasbon.html')

# Route untuk halaman profil
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/qr')
def qr():
    return render_template('qr.html')

@app.route('/submit_qr', methods=['POST'])
def submit_qr():
    data = request.get_json()
    qr_data = data.get('qr_data')

    if qr_data:
    # Process the QR code data (e.g., store in DB, validate, etc.)
        return jsonify({'redirect_url': url_for('result_qr', qr_data=qr_data)});

    # Respond to the client
    return jsonify({'error': 'No QR data found'}), 400

# Route to render the result page with QR data
@app.route('/result_qr')
def result_qr():
    qr_data = request.args.get('qr_data')
    if qr_data:
        return render_template('result_qr.html', qr_data=qr_data)
    else:
        return "No QR data available", 400
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
