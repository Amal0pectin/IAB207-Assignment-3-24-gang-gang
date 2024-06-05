from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, Flask
from .models import Event, Comment, User, Order
from .forms import EventForm, CommentForm, BookingForm, UpdateForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

event_bp = Blueprint('Event', __name__, url_prefix="/Events")

@event_bp.route('/<id>')
def details(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    form = CommentForm()
    bform = BookingForm()
    if not event:
       abort(404)
    return render_template('Events/details.html', event = event, bform=bform, form=form)

@event_bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    # call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data, description=form.description.data, 
    image=db_file_path, start_time=form.star_time.data, end_time=form.end_time.data,
    location=form.location.data, genre=form.genre.data, price=form.price.data, numberoftickets=form.numberoftickets.data, user_id=current_user.id)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new Event', 'success')
    return redirect(url_for('Event.create'))
  return render_template('Events/create.html', form=form)


def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'Static/img',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/img/' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path


@event_bp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form, associate the Comment's destination field
      # with the destination object from the above DB query
      comment = Comment(text=form.text.data, event = event, user = current_user)
      created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      # here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      # flash('Your comment has been added', 'success')  
      flash ('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('Event.details', id=id))

@event_bp.route('/<id>/booking', methods=['GET', 'POST'])  
@login_required
def booking(id):  
    form = BookingForm()  
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form, associate the Comment's destination field
      # with the destination object from the above DB query

      requestedtickets = form.ticketsbooked.data
      remainingtickets = event.numberoftickets

      if requestedtickets > remainingtickets:
        flash ('You are requesting more than the maximum ' + str(remainingtickets) + ' tickets', 'warning')
        return redirect(url_for('Event.details', id=event.id))

      order = Order(ticketsbooked=requestedtickets, booked_at=datetime.now(), event = event, user = current_user,)

      if requestedtickets == remainingtickets:
        event.status = 'Sold Out'
      
      #reduce event num tickets
      event.numberoftickets = event.numberoftickets - requestedtickets

      # here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(order) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      # flash('Your comment has been added', 'success')  
      flash ('Your order has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('Order.orders'))

@event_bp.route('/update/<id>', methods = ['GET', 'POST'])
@login_required
def update(id):
  print('Method type: ', request.method)
  event = db.session.scalar(db.select(Event).where(Event.id==id))
  form = UpdateForm(obj=event)
  if request.method == 'GET' and event:
    form.name.data = event.name
    form.description.data = event.description
    form.star_time.data = event.start_time
    form.end_time.data = event.end_time
    form.location.data = event.location
    form.genre.data = event.genre
    form.price.data = event.price
    form.numberoftickets.data = event.numberoftickets
    db_file_path = event.image

  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    query = Event(name=form.name.data, description=form.description.data, 
    image=db_file_path, start_time=form.star_time.data, end_time=form.end_time.data,
    location=form.location.data, genre=form.genre.data, price=form.price.data, numberoftickets=form.numberoftickets.data) 
    form.populate_obj(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new Event', 'success')
    return redirect(url_for('Event.update'))
  return render_template('Events/update.html', form=form)

