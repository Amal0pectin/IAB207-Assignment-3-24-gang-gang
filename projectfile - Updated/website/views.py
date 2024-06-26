from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events = events)

@main_bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.name.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
    


@main_bp.route('/genre_search')
def genre_search():
    if request.args['genre_search']:
        print(request.args['genre_search'])
        query = request.args['genre_search']
        events = db.session.scalars(db.select(Event).where(Event.genre.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))