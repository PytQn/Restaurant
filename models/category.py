from db import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    image = db.Column(db.String(5000))
    dishes = db.relationship('Dish', backref='category')
