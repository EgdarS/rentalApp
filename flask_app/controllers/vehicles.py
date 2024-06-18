from flask_app import app
from flask import render_template, redirect, session, request, flash, abort
from functools import wraps
from flask_app.models.user import User
from flask_app.models.vehicle import Vehicle
import os
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename

# Check if the format is right 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not User.is_admin(session['user_id']):
            return abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@app.route('/add/vehicle')
@admin_required
def addVehicle():
    return render_template('addVehicle.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create/vehicle', methods=['POST'])
@admin_required
def createVehicle():
    if not Vehicle.validate_vehicle(request.form):
        return redirect(request.referrer)
    
    if 'image' not in request.files:
        flash('No file part', 'image')
        return redirect(request.referrer)
    
    image = request.files['image']
    if image.filename == '':
        flash('No selected file', 'image')
        return redirect(request.referrer)
    
    if image and allowed_file(image.filename):
        filename1 = secure_filename(image.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time += filename1
        filename1 = time
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

    data = {
        'type': request.form['type'],
        'model': request.form['model'],
        'price': request.form['price'],
        'description': request.form['description'],
        'image': filename1,
        'user_id': session['user_id']
    }
    Vehicle.create(data)
    return redirect('/')


@app.route('/view/vehicle/<int:id>')
def viewVehicle(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'vehicle_id': id,
        'id': session['user_id']
    }
    vehicle = Vehicle.get_vehicle_by_id(data)
    loggedUser = User.get_user_by_id(data)
    usersWhoFavourited=Vehicle.getAllFavourites(data)
    return render_template('vehicle.html', vehicle=vehicle, loggedUser=loggedUser, usersWhoFavourited=usersWhoFavourited)

@app.route('/delete/vehicle/<int:id>')
@admin_required
def deleteVehicle(id):
    data={
        'vehicle_id':id,
        'id':session['user_id']
    }
    vehicle=Vehicle.get_vehicle_by_id(data)
    if not vehicle:
        return redirect('/')
    Vehicle.delete_all_favourites(data)
    Vehicle.delete_vehicle(data)
    return redirect('/')

@app.route('/edit/vehicle/<int:id>')
@admin_required
def editVehicle(id):
    data={
        'vehicle_id':id,
        'id':session['user_id']
    }
    vehicle=Vehicle.get_vehicle_by_id(data)
    return render_template('edit.html', vehicle=vehicle)

@app.route('/update/vehicle/<int:id>', methods=['POST'])
@admin_required
def updateVehicle(id):
    data={
        'vehicle_id':id,
        'id':session['user_id'],    
    }
    vehicle=Vehicle.get_vehicle_by_id(data)
    if not vehicle:
        return redirect('/')
    updateData={
        'type':request.form['type'],
        'model':request.form['model'],
        'price':request.form['price'],
        'description':request.form['description'],
        'id':id
    }
    if not Vehicle.validate_vehicle(updateData):
        return redirect(request.referrer)
    Vehicle.update_vehicle(updateData)
    #return redirect('/view/vehicle/'+str(id))           this redirects to the updated page after the changes 
    return redirect('/')
    
@app.route('/favourite/<int:id>')
def addFavourite(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'vehicle_id':id,
        'id': session['user_id']
    }
    print(f"Data for addVehicle: {data}")
    usersWhoFavourited=Vehicle.getAllFavourites(data)
    print(f"Users who favourited vehicle {id}: {usersWhoFavourited}")
    if session['user_id'] not in usersWhoFavourited:
        try:
            Vehicle.addFavourite(data)
        except Exception as e:
            print(f"Error adding favourite: {e}")
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/unfavourite/<int:id>')
def removeFavourite(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'vehicle_id':id,
        'id': session['user_id']
    }
    Vehicle.removeFavourite(data)
    return redirect(request.referrer)


