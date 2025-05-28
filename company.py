from src.main import db
from datetime import datetime

class Company(db.Model):
    """نموذج الشركة أو العلامة التجارية"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(200))  # مسار شعار الشركة
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع المستخدم (كل شركة لها مستخدم واحد كمدير)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # العلاقة مع المسابقات (شركة واحدة يمكن أن تنشئ عدة مسابقات)
    contests = db.relationship('Contest', backref='company', lazy='dynamic')
    
    def __repr__(self):
        return f'<Company {self.name}>'
