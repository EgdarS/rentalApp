from flask_app import app
from flask import render_template, redirect, session, request, flash, abort, url_for
from functools import wraps
from flask_app.models.user import User
from flask_app.models.vehicle import Vehicle
from flask_app.models.order import Order       
from datetime import timedelta, datetime


@app.route('/orders/new/<int:vehicle_id>')
def new_order(vehicle_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    vehicle = Vehicle.get_vehicle_by_id({'id': vehicle_id})
    
    # if not vehicle:
    #     flash('Vehicle not found', 'error')
    #     return redirect('/dashboard')
    
    all_vehicle_models = Vehicle.get_all_vehicle_models()
    
    return render_template('new_order.html', vehicle=vehicle, all_vehicle_models=all_vehicle_models)


@app.route('/orders/create', methods=['POST'])
def orders_create():
    if 'user_id' not in session:
        return redirect('/login')
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    vehicle_id = request.form['vehicle_id']
    user_id = session['user_id']
    
    vehicle = Vehicle.get_vehicle_by_id({'id': vehicle_id})
    price_per_day = vehicle['price']
    total_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
    total_price = total_days * price_per_day
    
    data = {
        'user_id': user_id,
        'vehicle_id': vehicle_id,
        'start_date': start_date,
        'end_date': end_date,
        'total_price': total_price
    }
    Order.create(data)
    flash('Order created successfully!', 'success')
    return redirect('/dashboard')

@app.route('/orders')
def view_orders():
    if 'user_id' not in session:
        return redirect('/login')
    orders = Order.get_by_user({'user_id': session['user_id']})
    return render_template('orders.html', orders=orders)
