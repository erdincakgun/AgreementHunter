from flask import Flask,  render_template, send_from_directory, jsonify, request
from utils import allowed_file, transcribe_and_extract_agreement_price
from config import PORT, UPLOAD_FOLDER, APP_KEY
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
from datetime import datetime
from flask_cors import CORS
from pathlib import Path
import requests
import sqlite3
import os

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = Flask(__name__)
app.secret_key = APP_KEY
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin/admin.html')


@app.route('/uploads/<path:path>', methods=['GET'])
def serve_uploads(path):
    return send_from_directory('uploads', path)


@app.route('/records', methods=['GET'])
def records():
    try:
        conn = sqlite3.connect('records.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM records ORDER BY date DESC')
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({'id': row[0], 'date': row[1], 'record_file': row[2],
                           'transcript': row[3], 'aggreement_price': row[4]})
        return jsonify(result)

    except Exception as e:
        return jsonify(message='Error fetching records', error=str(e)), 500

    finally:
        if conn:
            conn.close()


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        if 'file' not in request.files and 'url' not in request.form:
            return jsonify(message='No file or URL provided'), 400

        if 'file' in request.files:
            file = request.files['file']

            if file.filename == '':
                return jsonify(message='No file selected'), 400

        elif 'url' in request.form:
            file_url = request.form['url']
            parsed_url = urlparse(file_url)

            if not parsed_url.scheme or not parsed_url.netloc:
                return jsonify(message='Invalid URL'), 400

            try:
                response = requests.get(file_url, stream=True)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return jsonify(message='Error downloading file from URL',
                               error=str(e)), 500

            file = FileStorage(stream=response.raw,
                               filename=parsed_url.path.split('/')[-1])

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
            file_ext = Path(filename).suffix
            new_filename = f"{timestamp}{file_ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

            try:

                price, transcript = transcribe_and_extract_agreement_price(os.path.join(
                    app.config['UPLOAD_FOLDER'], new_filename))

                return jsonify(price=price, transcript=transcript), 200

            except Exception as e:
                return jsonify(message='Error processing audio file',
                               error=str(e)), 500

        else:
            return jsonify(message='Invalid file format'), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
