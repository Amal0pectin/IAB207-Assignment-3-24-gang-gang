from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
#from flask import login_required

order_bp = Blueprint('Order', __name__, url_prefix="/Order")

@login_required
@order_bp.route('/<id>')
def orders(id):
    # eventually we will query the database table 'destinations'for this id
    ## and get back all relevant information for that destination
    order = db.session.scalar(db.select(order).where(Order.user_id==current_user.id))

    form = CommentForm()
    if not order:
       abort(404) 
    return render_template('orders.html', order = order, form=form)