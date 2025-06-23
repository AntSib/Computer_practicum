from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired

class UploadKeysForm(FlaskForm):
    text = TextAreaField('Супер секретный текст', validators=[InputRequired()])
    submit = SubmitField('Загрузить zip-архив из шифра и ключа')

class UploadCypherForm(FlaskForm):
    key = FileField('key(.pem)', validators=[
        FileRequired(),
        # FileAllowed(['pem'], 'Только .pem файлы!')
    ])
    secret = FileField('secret(.bin)', validators=[
        FileRequired(),
        # FileAllowed(['bin'], 'Только .bin файлы!')
    ])
    submit = SubmitField('Расшифровать')