from flask import Flask, request
from config import Configuration
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Configuration)

@app.route('/')
def home():
    my_id = '1149817'
    return my_id + ', ' + str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


if __name__ == '__main__':
    app.run()
