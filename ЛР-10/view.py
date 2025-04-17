from app import app
from flask import render_template, request, jsonify
from models import UploadForm
import base64
import io
import json
from PIL import Image, ImageDraw


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    author = '1149817'
    return jsonify({'author': author})

@app.route('/makeimage', methods=['GET', 'POST'])
def img_size2json():
    form = UploadForm()
    form.process()
    return render_template('form.html', form=form)

@app.route('/sendimage', methods=['POST'])
def sendimage():
    if request.method == 'POST':
        if not (request.json['width'].isdigit() and request.json['height'].isdigit()):
            return jsonify({"message": "Invalid image size"})

        width: int = int(request.json['width'])
        height: int = int(request.json['height'])

        img = Image.new('RGB', (width, height), (0, 0, 0))
        d = ImageDraw.Draw(img)

        d.text((width / 2, height / 2), "Hello World", fill=(255, 255, 255))

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return jsonify({"image": f"data:image/jpeg;base64,{img_str}"})
