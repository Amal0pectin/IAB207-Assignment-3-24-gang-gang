from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeLocalField, RadioField, DecimalField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create new Event
class EventForm(FlaskForm):
  name = StringField('Artist', validators=[InputRequired()])
  description = TextAreaField('Description', validators = [InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  start_time = DateTimeLocalField('Start Time', validators=[InputRequired()])
  end_time = DateTimeLocalField('End Time', validators=[InputRequired()])
  location = StringField('Event Location', validators=[InputRequired()])
  genre = SelectField('Genre', validators=[InputRequired()], choices = [('HipHop'), ('Pop'), ('Rock'), ('Metal'), ('Indie'), ('Folk'), ('EDM')])
  price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0, max=1000)])
  numberoftickets = IntegerField('Number of Tickets', validators=[InputRequired(), NumberRange(min=1, max=50000)])
  submit = SubmitField("Create")
  
# Bookings

class BookingForm (FlaskForm):
  ticketsbooked = IntegerField('Number of Tickets', validators=[InputRequired(), NumberRange(min=1, max=10)])
  delivery_type = RadioField('Choose Delivery Option', validators=[InputRequired()], choices=[('Mobile Ticket (via SMS)','$8.50'),('Print-At-Home (PDF)','$8.50'),('Venue / Pre-Paid Collection Outlet', '$11.50') ])
  submit = SubmitField("Book")

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

# User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')
  current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Update Event
class UpdateForm(FlaskForm):
  name = StringField('Artist', validators=[InputRequired()])
  description = TextAreaField('Description', validators = [InputRequired()])
  start_time = DateTimeLocalField('Start Time', validators=[InputRequired()])
  end_time = DateTimeLocalField('End Time', validators=[InputRequired()])
  location = StringField('Event Location', validators=[InputRequired()])
  genre = SelectField('Genre', validators=[InputRequired()], choices = [('HipHop'), ('Pop'), ('Rock'), ('Metal'), ('Indie'), ('Folk'), ('EDM')])
  price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0, max=1000)])
  numberoftickets = IntegerField('Number of Tickets', validators=[InputRequired(), NumberRange(min=1, max=50000)])
  submit = SubmitField("Update")


class GenreFilterForm(FlaskForm):
    genre = SelectField('Genre', validators=[InputRequired()], choices=[
        ('All', 'All'),
        ('HipHop', 'HipHop'),
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Metal', 'Metal'),
        ('Indie', 'Indie'),
        ('Folk', 'Folk'),
        ('EDM', 'EDM')])
    submit = SubmitField("Search genre")