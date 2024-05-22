from flask import Blueprint, render_template
from .models import Event
from . import db
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalar(db.select(Event)).all()
    return render_template('index.html', events = events)