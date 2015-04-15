from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/hello.html') 
def hello_world(): 
    return 'Hello Sunshine!'

if __name__ == '__main__':
    app.run(debug=True)