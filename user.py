from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.main import db

class User(db.Model, UserMixin):
    """نموذج المستخدم الأساسي"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    
    # العلاقة مع الشركات (مستخدم واحد يمكن أن يدير شركة واحدة)
    company = db.relationship('Company', backref='admin', uselist=False)
    
    def set_password(self, password):
        """تعيين كلمة المرور المشفرة"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
