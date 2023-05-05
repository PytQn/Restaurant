from db import db
from datetime import datetime as dt


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_delivered = db.Column(db.Boolean, default=False)
    address = db.Column(db.Text(100))
    comment = db.Column(db.Text(200))
    created = db.Column(db.DateTime, default=dt.now)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), unique=True)
