from flask import Flask, request
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
