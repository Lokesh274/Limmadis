#Used AI for the template creation and some error handling
#Prompt used for db creation: how to create a table in the db with flask application
#used Reference from week7 slides to for library downloads and route methods for the login and signup pages
#https://uab.instructure.com/courses/1625351/files/folder/lecture/week_07?preview=75734758

from flask import Flask, render_template, request, redirect, url_for, session
import re  
from models import db, User  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SQLAlchemy with the Flask app
db.init_app(app)


# Source: Regular expression pattern adapted from OWASP Password Special Characters guidance
# https://owasp.org/www-community/password-special-characters
PASSWORD_REGEX = (
    r'^(?=.*[a-z])'   
    r'(?=.*[A-Z])'    
    r'(?=.*\d)'       
    r'.{8,}$'         
)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('secret_page'))
        else:
            return 'Invalid credentials. Please try again.'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
 
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validate password against the regex pattern
        if re.match(PASSWORD_REGEX, password):
            if password == confirm_password:
                existing_user = User.query.filter_by(email=email).first()
                if not existing_user:
                    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('thankyou'))
                else:
                    return 'Email address already in use. Please use a different email.'
            else:
                return 'Passwords do not match. Please try again.'
        else:
            return 'Password must contain at least one lowercase letter, one uppercase letter, one digit, and be at least 8 characters long.'
        
    return render_template('signup.html')

@app.route('/secretPage')
def secret_page():
 
    if 'user_id' in session:
        return render_template('secretPage.html')
    return redirect(url_for('login'))

@app.route('/thankyou')
def thankyou():
 
    return render_template('thankyou.html')

@app.route('/logout')
def logout():
 
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
