from db import db


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='cart')
    delivery = db.relationship('Delivery', backref='cart', uselist=False)
