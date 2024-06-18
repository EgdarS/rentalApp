from flask_app import app
from flask import render_template, redirect, session, request, flash, abort, url_for
from functools import wraps
from flask_app.models.user import User
from flask_app.models.vehicle import Vehicle
from flask_app.models.order import Order
from flask_bcrypt import Bcrypt        
from datetime import timedelta, datetime
import pytz

bcrypt = Bcrypt(app)

app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


@app.before_request
def session_management():
    session.permanent = True
    if 'user_id' in session:
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        last_activity = session.get('last_activity', utc_now)
        session['last_activity'] = utc_now
        if (utc_now - last_activity).total_seconds() > 30 * 60: 
            session.clear()
            return redirect('/login')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            abort(403)
        user_id = session['user_id']
        loggedAdmin = User.is_admin(user_id) 
        if not loggedAdmin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def controller():
    if 'user_id' not in session:
        return redirect('/logout')
    return redirect('/dashboard')

@app.route('/login')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginUser():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if not user: 
        flash('This user does not exist! Check your email', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Invalid password!', 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    session['role'] = user['role']  # Store the role in the session
    return redirect('/')

@app.route('/register', methods=['POST'])
def registerUser():
    if 'user_id' in session:
        return redirect('/')
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    user = User.get_user_by_email(request.form)
    if user:
        flash('This user already exists! Try another email.', 'emailRegister')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    admin_data = {
        'username': 'Admin User',
        'role': 'admin',
    }
    vehicles = Vehicle.getAllVehicles()
    return render_template('admin_dashboard.html', loggedAdmin=admin_data,)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    vehicles = Vehicle.getAllVehicles()
    data = {
        'id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    usersWhoFavourited = Vehicle.getAllFavourites(data)
    return render_template('dashboard.html', vehicles=vehicles, loggedUser=loggedUser, usersWhoFavourited=usersWhoFavourited)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
