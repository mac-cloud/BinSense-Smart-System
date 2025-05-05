# Import Dependencies
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify, send_from_directory
import main
import urllib.request
from werkzeug.utils import secure_filename
from main import getPrediction
import os
import secrets

# Path to the file where the secret key will be stored
secret_key_file = 'secret_key.txt'

def generate_secret_key():
    new_key = secrets.token_hex(16)
    with open(secret_key_file, 'w') as f:
        f.write(new_key)
    return new_key

def load_secret_key():
    if os.path.exists(secret_key_file):
        with open(secret_key_file, 'r') as f:
            return f.read().strip()
    else:
        return generate_secret_key()

#################################################
# Flask Setup
#################################################

UPLOAD_FOLDER = '/home/mac-aphid/Videos/4th-YEAR-PROJECT/waste-classification-model/static'

app = Flask(__name__)
app.secret_key = load_secret_key()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to HTML
@app.route('/')
def index():
    language = request.args.get('lang', 'en')
    return render_template('index.html', language=language)

# Route for uploading image
@app.route("/", methods=['POST'])
def submit_image():
    if request.method == 'POST':
        language = request.form.get('language', 'en')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index', lang=language))
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(url_for('index', lang=language))
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            answer, probability_results, filename = getPrediction(filename)
            flash(answer)
            flash(probability_results)
            flash(filename)
            return redirect(url_for('index', lang=language))

# Voice text classification endpoint
@app.route('/classify', methods=['POST'])
def classify_text():
    data = request.get_json()
    item_name = data.get('item', '').lower()

    # Very simple mock classification logic
    if "banana" in item_name or "apple" in item_name or "peel" in item_name:
        category = "organic"
        message = "This is organic waste. Please compost it."
    elif "plastic" in item_name or "bottle" in item_name or "cardboard" in item_name:
        category = "recyclable"
        message = "This is recyclable. Rinse it before recycling."
    else:
        category = "unknown"
        message = "Item not recognized. Please try again."

    return jsonify({'category': category, 'message': message})

@app.route('/translations/<filename>')
def serve_translation(filename):
    return send_from_directory('translations', filename)

if __name__ == "__main__":
    app.run(debug=True)
