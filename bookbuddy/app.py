from flask import Flask, render_template, request,url_for,redirect
import pickle
import numpy as np
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
current_directory = os.path.dirname(os.path.realpath(__file__))

popular_path = os.path.join(current_directory, 'popular.pkl')
pt_path = os.path.join(current_directory, 'pt.pkl')
books_path = os.path.join(current_directory, 'books.pkl')
similarity_score_path = os.path.join(current_directory, 'similarity_score.pkl')

popular_df = pickle.load(open(popular_path, 'rb'))
pt = pickle.load(open(pt_path, 'rb'))
books = pickle.load(open(books_path, 'rb'))
similarity_score = pickle.load(open(similarity_score_path, 'rb'))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


# Model
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    password = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Name: {self.first_name}, Age: {self.age}"

# Create the database tables within the application context
with app.app_context():
    db.create_all()


@app.route('/home')
def index():
    print(popular_df.columns)

    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend',methods=['GET',"POST"])
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index_array = np.where(pt.index == user_input)[0]

    if len(index_array) == 0:
        error_message = f"Book '{user_input}' not found. Please try another book."
        return render_template('error.html', error_message=error_message)

    index = index_array[0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)

@app.route('/romantic')
def romantic():
    return render_template('romantic.html')

@app.route('/horror')
def horror():
    return render_template('horror.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        gender= request.form.get('gender')
        age= request.form.get('age')
        phone=request.form.get('phone')
        password= request.form.get('password')
        # Extract other form fields as needed
        print(f"Name: {name}, Email: {email}, Gender: {gender}, Age: {age}, Phone: {phone}, Password: {password}")


        # Create a new instance of the Profile model
        new_profile = Profile(name=name, email=email,age=age,gender=gender,password=password,phone=phone)
        # Add the new profile to the database session
        db.session.add(new_profile)
        # Commit the changes to the database
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/welcome")
def welcome():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/login',methods=['GET','POST'])
def login():
     if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the user exists in the database and the password matches
        user = Profile.query.filter_by(email=email, password=password).first()
        if user:
            # If the user is valid, redirect to the home page
            print("User found")
            return redirect(url_for('welcome'))
        else:
            print("User not found")
            # If the user is not valid, render the login page with an error message
            # return render_template('login.html', error="Invalid email or password.")
    
    
     return render_template('login.html')
 
@app.route('/')
def landing():
    return render_template('landing.html')

# Define other routes

if __name__ == '__main__':
    app.run(debug=True)
