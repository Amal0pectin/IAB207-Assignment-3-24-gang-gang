from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User, Order
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

order_bp = Blueprint('Order', __name__, url_prefix="/Order")

@login_required
@order_bp.route('/id')
def orders():
    # eventually we will query the database table 'destinations'for this id
    ## and get back all relevant information for that destination
    orders = db.session.scalars(db.select(Order).join(Event).where(Order.user_id==current_user.id)).all()
    if not orders:
        return redirect(url_for('auth.login'))
    return render_template(url_for('orders.html', id=id))