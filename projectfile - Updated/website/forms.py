from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeLocalField, RadioField, DecimalField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create new Event
class EventForm(FlaskForm):
  name = StringField('Artist', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators = [InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  star_time = DateTimeLocalField('Start Time', validators=[InputRequired()])
  end_time = DateTimeLocalField('End Time', validators=[InputRequired()])
  location = StringField('Event Location', validators=[InputRequired()])
  genre = StringField('Genre', validators=[InputRequired()])
  price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0, max=1000)])
  numberoftickets = IntegerField('Number of Tickets', validators=[InputRequired(), NumberRange(min=1, max=50000)])
  submit = SubmitField("Create")

# Bookings

class BookingForm (FlaskForm):
   ticket_type = RadioField('Select Ticket', choices=[('Best Available','(any price) From $200'),('A Reserve ','$400'),('B Reserve', '$300'), ('C Reserve', '$200')])

   delivery_type = RadioField('Choose Delivery Option', choices=[('Mobile Ticket (via SMS)','$8.50'),('Print-At-Home (PDF)','$8.50'),('Venue / Pre-Paid Collection Outlet', '$11.50') ])
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



