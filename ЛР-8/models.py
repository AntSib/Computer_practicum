from wtforms import Form, StringField


class UploadForm(Form):
    image = FileField(u'Image')
    description = TextAreaField(u"Принимаемые форматы: .jpg, .jpeg, .png")
