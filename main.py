import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import os

# إنشاء تطبيق Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketing_contests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إنشاء قاعدة البيانات
db = SQLAlchemy(app)

# إعداد نظام تسجيل الدخول
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# استيراد النماذج
from src.models.user import User
from src.models.company import Company
from src.models.contest import Contest
from src.models.participant import Participant

# استيراد المسارات
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
from src.routes.contests import contests_bp
from src.routes.public import public_bp

# تسجيل المسارات
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(contests_bp)
app.register_blueprint(public_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """الصفحة الرئيسية للتطبيق"""
    active_contests = Contest.query.filter_by(is_active=True).all()
    return render_template('public/index.html', contests=active_contests)

@app.errorhandler(404)
def page_not_found(e):
    """صفحة الخطأ 404"""
    return render_template('public/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """صفحة الخطأ 500"""
    return render_template('public/500.html'), 500

# إنشاء قاعدة البيانات عند تشغيل التطبيق
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
