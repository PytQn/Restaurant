from flask import render_template, url_for, request, redirect
from flask_login import login_user, current_user, login_required, logout_user
from db import db
from models.cart import Cart
from models.category import Category
from models.delivery import Delivery
from models.dish import Dish
from models.user import User
from models.item import Item


def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user != None and user.is_staff == False:
            if user.password == request.form['password']:
                login_user(user)
                return redirect(url_for('homepage'))
            else:
                return 'Wrong password'
        else:
            return 'User not found'
    return render_template('users/login.html')


def signup():
    if request.method == 'POST':
        try:
            if request.form['password'] == request.form['password_confirm']:
                new_user = User(
                    username=request.form['username'],
                    password=request.form['password'],
                    first_name=request.form['first_name'],
                    last_name=request.form['last_name'],
                    email=request.form['email']
                )
                db.session.add(new_user)
                db.session.commit()
            return redirect(url_for('homepage'))
        except Exception as e:
            return redirect(url_for('homepage'))
    return render_template('users/signup.html')


@login_required
def edit():
    if current_user.is_staff == True:
        return redirect(url_for('admins.admin_login'))
    id = current_user.id
    user = User.query.get(id)
    if request.method == 'POST':
        user.password = request.form['password']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('users.user'))
    return render_template('users/edit.html')


@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


def category(id):
    category = Category.query.get(id)
    if request.method == 'POST':
        if current_user.is_staff == True:
            return redirect(url_for('admins.admin_login'))
        cart = Cart.query.filter_by(
            user_id=current_user.id, delivery=None).first()
        if cart:
            item = Item.query.filter_by(
                dish_id=request.form['dish'], cart_id=cart.id).first()
            if item:
                item.amount += int(request.form['amount'])
            else:
                item = Item(
                    dish_id=request.form['dish'],
                    amount=request.form['amount']
                )
                cart.items.append(item)
        else:
            new_cart = Cart(user_id=current_user.id)
            item = Item(
                dish_id=request.form['dish'],
                amount=request.form['amount']
            )
            new_cart.items.append(item)
            db.session.add(new_cart)
        db.session.commit()
    return render_template('users/category.html', category=category)


@login_required
def user():
    if current_user.is_staff == True:
        return redirect(url_for('admins.admin_login'))
    return render_template('users/user.html')


@login_required
def history():
    if current_user.is_staff == True:
        return redirect(url_for('admins.admin_login'))
    deliveries = Delivery.query.join(Cart).filter(
        Cart.user_id == current_user.id).all()
    dishes = Dish.query.all()
    summary = 0
    for delivery in deliveries:
        for item in delivery.cart.items:
            for dish in dishes:
                if dish.id == item.dish_id:
                    summary += item.amount*dish.price
    return render_template('users/history.html', deliveries=deliveries, dishes=dishes, summary=summary)


@login_required
def cart(id):
    if current_user.is_staff == True:
        return redirect(url_for('admins.admin_login'))
    cart = Cart.query.filter_by(
        user_id=id, delivery=None).first()
    dishes = Dish.query.all()
    if request.method == 'POST':
        item = Item.query.filter_by(id=request.form['item']).first()
        db.session.delete(item)
        db.session.commit()
    summary = 0
    if cart != None:
        for item in cart.items:
            for dish in dishes:
                if dish.id == item.dish_id:
                    summary += item.amount*dish.price
    return render_template('users/cart.html', cart=cart, dishes=dishes, summary=summary)


@login_required
def show_delivery(id):
    if current_user.is_staff == True:
        return redirect(url_for('admins.admin_login'))
    delivery = Delivery.query.get(id)
    dishes = Dish.query.all()
    summary = 0
    for item in delivery.cart.items:
        for dish in dishes:
            if dish.id == item.dish_id:
                summary += item.amount*dish.price
    return render_template('users/show_delivery.html', delivery=delivery, dishes=dishes, summary=summary)


@login_required
def order(id):
    if current_user.is_staff == True:
        return redirect(url_for('admins.admin_login'))
    cart = Cart.query.filter_by(
        id=id, delivery=None).first()
    if request.method == 'POST':
        new_delivery = Delivery(
            address=request.form['address'],
            comment=request.form['comment'],
            cart_id=id,
        )
        db.session.add(new_delivery)
        db.session.commit()
        return redirect(url_for('users.show_delivery', id=new_delivery.id))
    return render_template('users/order.html', cart=cart)
