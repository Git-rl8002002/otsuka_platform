#!/usr/bin/python3

from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('test.html')





if __name__ == '__main__':
    #socket_.run(app , host="0.0.0.0" , port=8090 , debug=True)
    app.run(app , host="0.0.0.0" , port=8090 , debug=True)