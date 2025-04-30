from app import app
from flask import render_template, request, jsonify
from models import UploadForm
from cipher import caesar_encrypt, caesar_decrypt


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    author = '1149817'
    return jsonify({'author': author})

@app.route('/decypher', methods=['GET', 'POST'])
def decypher_view():
    if request.method == 'POST':
        if not (request.form.get('key').isdigit() or not request.form.get('secret')):
            return jsonify({"message": "Invalid key or secret"})

        key = int(request.form.get('key'))
        message = request.form.get('secret')
        
        message = caesar_decrypt(message, key)

        return jsonify({"message": message})

    form = UploadForm()
    form.process()
    return render_template('form.html', form=form)
    
@app.route('/Encypher', methods=['GET', 'POST'])
def cipher_view():
    if request.method == 'POST':
        if not (request.form.get('key') or not request.form.get('secret')):
            return jsonify({"message": "Invalid key or secret"})

        key = int(request.form.get('key'))
        message = request.form.get('secret')
        
        message = caesar_encrypt(message, key)

        return jsonify({"message": message})
    
    form = UploadForm()
    form.process()

    return render_template('form encoder.html', form=form)
