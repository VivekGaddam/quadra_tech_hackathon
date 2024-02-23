from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class SignUpForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    submit = SubmitField('Sign Up')

# Create the database tables outside the route handlers
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            new_volunteer = Volunteer(name=form.name.data, email=form.email.data)
            db.session.add(new_volunteer)
            db.session.commit()
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists. Please use a different email.', 'danger')

    return render_template('signup.html', form=form)

@app.route('/resources')
def view_resources():
    resources = Volunteer.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
