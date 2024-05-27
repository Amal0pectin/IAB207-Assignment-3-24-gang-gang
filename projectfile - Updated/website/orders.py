from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User, Order
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
#from flask import login_required

order_bp = Blueprint('Order', __name__, url_prefix="/Order")

@login_required
@order_bp.route('/BookingHistory')
def orders():
    # eventually we will query the database table 'destinations'for this id
    ## and get back all relevant information for that destination
    orders = db.session.scalars(db.select(Order).join(Event).where(Order.user_id==current_user.id)).all()

    print(orders)
    return render_template('orders.html', orders=orders)