from flask import Blueprint
from controllers.admin import admin_login, admin, list_dishes, add_dish, edit_dish, delete_dish, list_categories, add_category, edit_category, delete_category, all_deliveries, delivered

admins_bp = Blueprint('admins', __name__)

admins_bp.add_url_rule(
    '/admin_login', view_func=admin_login, methods=['GET', 'POST'])
admins_bp.add_url_rule('/admin', view_func=admin)
admins_bp.add_url_rule('/admin/dishes', view_func=list_dishes)
admins_bp.add_url_rule('/admin/dishes/add',
                       view_func=add_dish, methods=['GET', 'POST'])
admins_bp.add_url_rule('/admin/dishes/<int:id>/edit',
                       view_func=edit_dish, methods=['GET', 'POST'])
admins_bp.add_url_rule('/admin/dishes/<int:id>/delete',
                       view_func=delete_dish, methods=['GET', 'POST'])
admins_bp.add_url_rule('/admin/categories', view_func=list_categories)
admins_bp.add_url_rule('/admin/categories/add',
                       view_func=add_category, methods=['GET', 'POST'])
admins_bp.add_url_rule('/admin/categories/<int:id>/edit',
                       view_func=edit_category, methods=['GET', 'POST'])
admins_bp.add_url_rule('/admin/categories/<int:id>/delete',
                       view_func=delete_category, methods=['GET', 'POST'])
admins_bp.add_url_rule('/admin/delivery', view_func=all_deliveries)
admins_bp.add_url_rule(
    '/admin/delivery/<int:id>/delivered', view_func=delivered, methods=['POST'])
