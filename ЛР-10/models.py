from wtforms import Form, StringField, SubmitField


class UploadForm(Form):
    width = StringField("Width", default="150")
    height = StringField("Height", default="120")
    submit = SubmitField("Отправить")

