from flask import Flask, request
from config import Configuration
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Configuration)

csrf = CSRFProtect(app)
