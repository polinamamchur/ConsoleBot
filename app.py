from flask import Flask
from main import run

app = Flask(__name__)

@app.route('/')
def index():
    run()
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0,0,0,0', debug=True)
