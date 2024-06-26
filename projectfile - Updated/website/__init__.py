#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime


db = SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    # Should be set to false in a production environment
    app.debug = True
    app.secret_key = 'somesecretkey'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    #initialize db with flask app
    db.init_app(app)

    Bootstrap5(app)

    UPLOAD_FOLDER = '/Static/Img'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    #initialize the login manager
    login_manager = LoginManager()
    
    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.main_bp)

    from . import events
    app.register_blueprint(events.event_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import orders
    app.register_blueprint(orders.order_bp)

    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)

    @app.errorhandler(404)
    def page_not_found(e):
    # note that we set the 404 status explicitly
        return render_template('404.html', error=e)

    @app.errorhandler(500)
    def internal_server_error(e):
    # note that we set the 500 status explicitly
        return render_template('404.html', error=e)
    
    return app
