from flask import Blueprint
from controllers.user import login, signup, logout, category, user, history, cart, show_delivery, order, edit

users_bp = Blueprint('users', __name__)

users_bp.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
users_bp.add_url_rule('/signup', view_func=signup, methods=['GET', 'POST'])
users_bp.add_url_rule('/user/edit', view_func=edit, methods=['GET', 'POST'])
users_bp.add_url_rule('/logout', view_func=logout)
users_bp.add_url_rule('/category/<int:id>',
                      view_func=category, methods=['GET', 'POST'])
users_bp.add_url_rule('/user', view_func=user)
users_bp.add_url_rule('/user/history', view_func=history)
users_bp.add_url_rule('/user/<int:id>/cart',
                      view_func=cart, methods=['GET', 'POST'])
users_bp.add_url_rule('/user/order/<int:id>',
                      view_func=order, methods=['GET', 'POST'])
users_bp.add_url_rule('/user/show_delivery/<int:id>', view_func=show_delivery)
