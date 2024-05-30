from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User, Order
from .forms import EventForm, CommentForm, UpdateForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

order_bp = Blueprint('Order', __name__, url_prefix="/Order")


@order_bp.route('/<id>')
@login_required
def orders(id):
    # eventually we will query the database table 'destinations'for this id
    ## and get back all relevant information for that destination
    orders = db.session.scalars(db.select(Order).where(Order.id==id))
    form = UpdateForm()
    if not orders:
        abort(404)
    return render_template(url_for('Order.orders', id=id))