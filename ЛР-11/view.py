from app import app
from flask import render_template, request, jsonify, send_file
from models import UploadKeysForm, UploadCypherForm
from cypher import generate_rsa_keys, encrypt_rsa, decrypt_rsa, serialize_private_key
from io import BytesIO
import zipfile


@app.route('/login')
def login():
    author = '1149817'
    return jsonify({'author': author})



@app.route('/')
def index():
    return render_template('index.html')

'''
@app.route('/cypher_worker', methods=['POST'])
def cypher():
    text = request.form['text']
    priv_key, pub_key = generate_keys()
    encrypted = encrypt_message(text, pub_key)

    # Сериализация ключа
    private_bytes = serialize_private_key(priv_key)

    # Упаковка в ZIP без преобразований
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr('secret', encrypted)
        zf.writestr('key', private_bytes)
    zip_buffer.seek(0)

    return send_file(
        zip_buffer, 
        mimetype='application/zip', 
        as_attachment=True, 
        download_name='encrypted_bundle.zip'
    )
'''

@app.route('/cypher', methods=['GET', 'POST'])
def cypher_view():
    form = UploadKeysForm()

    if request.method == 'GET':
        return render_template('cypher.html', form=form)

    if form.validate_on_submit():
        # if not request.request.form['text']:
        #     return jsonify({"message": "Invalid key or secret"})

        private_key, public_key = generate_rsa_keys()

        message = form.text.data.encode('utf-8')
        encypted = encrypt_rsa(message, public_key)

        private_bytes = serialize_private_key(private_key)
        # message = encrypt_string(message, public_key)

        # print(message) # bytes
        # print(private_key) # str

        # file = io.BytesIO()
        # file.write(message)
        # file.seek(0)

        # return jsonify({"key": private_key, "message": file})
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr('secret', encypted)
            zf.writestr('key', private_bytes)
        zip_buffer.seek(0)

        return send_file(
            zip_buffer, 
            mimetype='application/zip', 
            as_attachment=True, 
            download_name='encrypted_bundle.zip'
        )


'''
@app.route('/decypher', methods=['GET', 'POST'])
def decypher():
    if request.method == 'GET':
        return render_template('decrypt.html')

    key_file = request.files['key']
    secret_file = request.files['secret']

    private_key_pem = key_file.read()
    encrypted_data = secret_file.read()

    import base64
    print(f"Encrypted data: {base64.b64encode(encrypted_data).decode('utf-8')}")
    print(f"Private key: {private_key_pem.decode('utf-8')}")

    try:
        decrypted_text = decrypt_rsa(encrypted_data, private_key_pem)
        return decrypted_text
    except Exception as e:
        raise e
'''

@app.route('/decypher', methods=['GET'])
def decypher_form():
    form = UploadCypherForm()
    return render_template('decypher.html', form=form)

@app.route('/decypher_worker', methods=['POST'])
def decypher_view():
    form = UploadCypherForm()

    if form.validate_on_submit():
        key_file = form.key.data
        secret_file = form.secret.data

        private_key_pem = key_file.read()
        encrypted_data = secret_file.read()

        try:
            result = decrypt_rsa(encrypted_data, private_key_pem)
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'result': f'Ошибка при дешифровке: {str(e)}'}), 400
    else:
        return jsonify({'result': 'Неверный формат формы'}), 400
