from wtforms import Form, StringField, SubmitField


class UploadForm(Form):
    key = StringField("Key", default="123")
    secret = StringField("Secret", default="Hello, World")
    submit = SubmitField("Отправить")
