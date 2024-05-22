from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
#from flask import login_required

order_bp = Blueprint('Order', __name__, url_prefix="/Order")

@order_bp.route('/<id>')
def orders(id):
    # eventually we will query the database table 'destinations'for this id
    ## and get back all relevant information for that destination
    order = db.session.scalar(db.select(order).where(order.id==id))
    form = CommentForm()
    if not order:
       abort(404) 
    return render_template('Bookings.html', order = order, form=form)