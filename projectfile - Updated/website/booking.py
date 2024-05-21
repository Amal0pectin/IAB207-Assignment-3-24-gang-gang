from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
#from flask import login_required

book_bp = Blueprint('Bookings', __name__, url_prefix="/Booking")

@book_bp.route('/<id>')
def bookings(id):
    # eventually we will query the database table 'destinations'for this id
    ## and get back all relevant information for that destination
    book = db.session.scalar(db.select(User).where(User.id==id))
    form = CommentForm()
    if not book:
       abort(404) 
    return render_template('Bookings.html', book = book, form=form)