from flask import render_template, url_for, request, redirect
from flask_login import login_user, current_user, login_required
from db import db
from models.category import Category
from models.delivery import Delivery
from models.dish import Dish
from models.user import User
from werkzeug.utils import secure_filename


def admin_login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user != None and user.is_staff == True:
            if user.password == request.form['password']:
                login_user(user)
                return redirect(url_for('admins.admin'))
            else:
                return 'Wrong password'
        else:
            return 'User not found'
    return render_template('admins/a_login.html')


@login_required
def admin():
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    return render_template('admins/admin.html')


@login_required
def list_dishes():
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    dishes = Dish.query.all()
    return render_template('admins/dishes/a_dish.html', dishes=dishes)


@login_required
def add_dish():
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    categories = Category.query.all()
    if request.method == 'POST':
        f = request.files['image']
        if f:
            f.save('./static/image/'+secure_filename(f.filename))
            image_url = '/static/image/'+f.filename
        else:
            image_url = None
        dish = Dish(
            name=request.form['name'],
            category_id=request.form['category_id'],
            price=request.form['price'],
            description=request.form['description'],
            image=image_url,
            is_gluten_free=True if request.form.get(
                'is_gluten_free') else False,
            is_vegeterian=True if request.form.get(
                'is_vegeterian') else False
        )
        db.session.add(dish)
        db.session.commit()
        return redirect(url_for('admins.list_dishes'))
    return render_template('admins/dishes/a_dish_new.html', categories=categories)


@login_required
def edit_dish(id):
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    categories = Category.query.all()
    dish = Dish.query.get(id)
    if request.method == 'POST':
        f = request.files['image']
        if f:
            f.save('./static/image/'+secure_filename(f.filename))
            image_url = '/static/image/'+f.filename
        else:
            image_url = None
        dish.name = request.form['name']
        dish.category_id = request.form['category_id']
        dish.price = request.form['price']
        dish.description = request.form['description']
        dish.image = image_url
        dish.is_gluten_free = True if request.form.get(
            'is_gluten_free') else False
        dish.is_vegeterian = True if request.form.get(
            'is_vegeterian') else False
        db.session.commit()
        return redirect(url_for('admins.list_dishes'))
    return render_template('admins/dishes/a_dish_edit.html', dish=dish, categories=categories)


@login_required
def delete_dish(id):
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    dish = Dish.query.get(id)
    db.session.delete(dish)
    db.session.commit()
    return redirect(url_for('admins.list_dishes'))


@login_required
def list_categories():
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    categories = Category.query.all()
    return render_template('admins/categories/a_category.html', categories=categories)


@login_required
def add_category():
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    if request.method == 'POST':
        f = request.files['image']
        if f:
            f.save('./static/image/'+secure_filename(f.filename))
            image_url = '/static/image/'+f.filename
        else:
            image_url = None
        category = Category(
            name=request.form['name'],
            image=image_url
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admins.list_categories'))
    return render_template('admins/categories/a_category_new.html')


@login_required
def edit_category(id):
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    category = Category.query.get(id)
    if request.method == 'POST':
        f = request.files['image']
        if f:
            f.save('./static/image/'+secure_filename(f.filename))
            image_url = '/static/image/'+f.filename
        else:
            image_url = None
        category.name = request.form['name']
        category.image = image_url
        db.session.commit()
        return redirect(url_for('admins.list_categories'))
    return render_template('admins/categories/a_category_edit.html', category=category)


@login_required
def delete_category(id):
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('admins.list_categories'))


@login_required
def all_deliveries():
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    deliveries = Delivery.query.all()
    dishes = Dish.query.all()
    users = User.query.all()
    summary = 0
    for delivery in deliveries:
        for item in delivery.cart.items:
            for dish in dishes:
                if dish.id == item.dish_id:
                    summary += item.amount*dish.price
    return render_template('admins/deliveries.html', deliveries=deliveries, dishes=dishes, users=users, summary=summary)


@login_required
def delivered(id):
    if current_user.is_staff == False:
        return redirect(url_for('homepage'))
    delivery = Delivery.query.get(id)
    if request.method == 'POST':
        delivery.is_delivered = True if request.form.get(
            'delivered') else False
        db.session.commit()
    return redirect(url_for('admins.all_deliveries'))
