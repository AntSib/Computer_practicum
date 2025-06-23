from wtforms import Form, StringField, SubmitField


class UploadForm(Form):
    width = StringField("Width", default="150")
    height = StringField("Height", default="120")
    text = StringField("Text", default="Hello World")
    submit = SubmitField("Отправить")

