from db import db

class Item(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    dish_id=db.Column(db.Integer, db.ForeignKey('dish.id'))
    cart_id=db.Column(db.Integer, db.ForeignKey('cart.id'))
    amount=db.Column(db.Integer, nullable=False)
