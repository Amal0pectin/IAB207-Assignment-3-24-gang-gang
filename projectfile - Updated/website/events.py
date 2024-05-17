from flask import Blueprint, render_template, request, redirect, url_for
from travel.model import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

destbp = Blueprint('events', __name__, url_prefix="/events")

@destbp.route('/<id>')
def detials(id):
    # eventually we will query the database table 'destinations'for this id
    ## and get back all relevant information for that destination
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    cform = CommentForm()
    return render_template('events/Event Detials.html', destination = destination, form=cform)

@destbp.route('/create', methods = ['GET', 'POST'])
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    # call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,
                               description=form.description.data,
                               image=db_file_path,
                               start_time=form.star_time.data,
                               end_time=form.end_time.data)
    # add the object to the db session
    db.session.add(events)
    # commit to the database
    db.session.commit()
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)


def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
def comment(id):  
    form = CommentForm()  
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form, associate the Comment's destination field
      # with the destination object from the above DB query
      comment = Comment(text=form.text.data, destination=destination) 
      # here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      # flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=id))

