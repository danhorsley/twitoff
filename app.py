"""main application and routing logic for twitoff"""
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import *


def create_app():
    """Create and configure instance of the Flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = 'debug'
    DB.init_app(app)
  
    @app.route('/')
    def root():
        #return 'Welcome to TwitOff!!'
        users = User.query.all()
        check_list = [1,2,3,4]
        return render_template('base2.html', title='Home',users=users)
   
    @app.route('/reset')
    def reset():
        DB.drop_all
        DB.create_all()
        return 'Welcome to TwitOff reset!!'

    @app.route('/user', methods = ['POST'])
    @app.route('/user/<name>', methods = ['GET'])
    def user(name=None, message='',tweets=[]):
        name = name or request.values['user_name']
        try:
            if request.method =='POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
        return render_template('users.html', title=name, tweets = tweets, message = message)

    return app