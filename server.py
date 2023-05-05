from flask import Flask, render_template
from auth import login_manager
from db import db
from models.category import Category
from routes.admins import admins_bp
from routes.users import users_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'dkfu5647lsemgs66jsdg34654'

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def homepage():
    categories = Category.query.all()
    return render_template('homepage.html', categories=categories)


app.register_blueprint(users_bp)
app.register_blueprint(admins_bp)

app.run(debug=True)
