'''
Flask uses patterns to match the incoming request URL to the view that should
handle it. The view returns data that Flask turns into an outgoing response.
Flask can also go the other direction and generate a URL to a view based on its
name and arguments.

Here we create a 'Blueprint' to organize a group of views
Flaskr will have two blueprints, one for authentication functions and one
for the blog posts functions.
'''
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Create Blueprint caleld auth

bp = Blueprint('auth', __name__, url_prefix='/auth')

# view code for when the user visits the /auth/register URL, the register view
# will return HTML with a form for them to fill out. When they submit the form,
# it will validate their input and either show the form again with an error
# message or create the new user and go to the login page.

'''
REGISTER CODE
'''
# associate the URL /register with the register view function
# if user submits the form request.method will be 'POST'
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username'] # Dict  mapping for  form keys/values
        password = request.form['password']
        db = get_db()
        error = None
        # Validate user
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        # db.execute: db.execute takes a SQL query with ? placeholders for any
        # user input, and a tuple of values to replace the placeholders with.
        # For security, passwords should never be stored in the database
        # directly. Instead, generate_password_hash() is used to securely hash
        # the password, and that hash is stored.
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit() # save changes
            return redirect(url_for('auth.login'))
            # redirected to the login page. url_for() generates the URL for
            # the login view based on its name.
        flash(error) # message that can be retrieved when rendering the template.

    return render_template('auth/register.html')
'''
LOGIN CODE
'''
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        # The data is stored in a cookie that is sent to the browser, and the
        # browser then sends it back with subsequent requests. Flask securely
        # signs the data so that it can’t be tampered with.
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
'''
REQUEST CODE
'''
# a function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
# checks if a user id is stored in the session and gets that user’s data from
# the database, storing it on g.user, which lasts for the length of the request
'''
LOGOUT CODE
'''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
'''
REQUIRE LOGIN
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
