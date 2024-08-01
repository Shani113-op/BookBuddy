from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# @app.route('/')
# def index():
#     return "Hello world"

# @app.route('/login')
# def login():
#     return render_template('login.html')
    
# @app.route('/register')
# def register():
#     return render_template('register.html')
    

if  __name__ == "__main__":
    app.run(debug=True)