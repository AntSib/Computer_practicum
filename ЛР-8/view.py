from app import app
from flask import render_template, request, redirect, url_for, jsonify
import os
import json
from PIL import Image
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login')
def login():
    author = '1149817'
    return jsonify({'author': author})

@app.route('/size2json', methods=['GET', 'POST'])
def img_size2json():
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            return jsonify({"result":"invalid filetype"})       #
            
        if file and allowed_file(file.filename):
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                with Image.open(file_path) as img:
                    width, height = img.size

                os.remove(file_path)
            except Exception as e:
                print(e)
                return f"Error: {e}"
            else:
                return jsonify({'width': width, 'height': height})  #
        else:
            return jsonify({"result":"invalid filetype"})

    return render_template('form.html')



'''
FILE_PATH:  str = os.path.dirname(os.path.realpath(__file__))
PARENT_PATH:  str = os.path.abspath(os.path.join(FILE_PATH, os.pardir))

json_log:   str = 'db\\logger.json'
db_log:     str = 'db\\logtable.db'

json_log_path:str = os.path.join(PARENT_PATH, json_log)
db_log_path:str = os.path.join(PARENT_PATH, db_log)


@app.route('/', methods=['GET', 'POST'])
def myform():
    if request.method == 'POST':
        login = request.form.get('login')
        current_time = request.form.get('time')
        
        if not login or not current_time:
            return render_template('base.html', content='Oшибка! Не все поля заполнены!')
        try:
            # JSON
            data = {'login': login, 'time': current_time}
            if os.path.exists(json_log_path):
                with open(json_log_path, 'r', encoding='utf-8') as f:
                    try:
                        json_data = json.load(f)
                    except json.JSONDecodeError:
                        json_data = []
            else:
                json_data = []
            json_data.append(data)
            with open(json_log_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            
            # SQLite
            connection = sqlite3.connect(db_log_path)
            with db_connector(connection) as con:
                con.execute("INSERT INTO users (login, time) VALUES (?, ?)", (login, current_time))
        except Exception as e:
            print(e)
            return render_template('base.html', content='Oшибка! Данные не сохранены! Traceback: ' + str(e))
        
        return render_template('base.html', content='Данные успешно сохранены!')
    
    return render_template('form.html', default_login='1149817', current_time=datetime.now().strftime("%d.%m.%Y, %H:%M:%S"))
'''