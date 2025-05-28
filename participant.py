from src.main import db
from datetime import datetime

class Participant(db.Model):
    """نموذج المشارك في المسابقة"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    score = db.Column(db.Integer, default=0)
    answers = db.Column(db.Text)  # إجابات المشارك بتنسيق JSON
    completed = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع المسابقة (كل مشارك ينتمي لمسابقة واحدة)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))
    
    def __repr__(self):
        return f'<Participant {self.name}>'
