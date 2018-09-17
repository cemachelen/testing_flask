import os

from flask import Flask
from flask import current_app
# Import code
from . import db, auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='key',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    with app.app_context():
        # within this block, current_app points to app.
        print(current_app.name)
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # when following the flask tutorial make sure not to start a new app!
    # we only want one create_app()!!
    # Database
    db.init_app(app)
    # blueprints and autherization: view to register users and login and log out
    app.register_blueprint(auth.bp)
    return app
