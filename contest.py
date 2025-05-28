from src.main import db
from datetime import datetime
import json

class Contest(db.Model):
    """نموذج المسابقة التسويقية"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    rules = db.Column(db.Text)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    max_participants = db.Column(db.Integer, default=0)  # 0 يعني غير محدود
    prize_description = db.Column(db.Text)
    contest_type = db.Column(db.String(50))  # نوع المسابقة (اختبار، لغز، تحدي، إلخ)
    template_data = db.Column(db.Text)  # بيانات القالب بتنسيق JSON
    custom_css = db.Column(db.Text)  # CSS مخصص للمسابقة
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع الشركة (كل مسابقة تنتمي لشركة واحدة)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    
    # العلاقة مع المشاركين (مسابقة واحدة يمكن أن يشارك فيها عدة مشاركين)
    participants = db.relationship('Participant', backref='contest', lazy='dynamic')
    
    def get_template_data(self):
        """استرجاع بيانات القالب كقاموس"""
        if self.template_data:
            return json.loads(self.template_data)
        return {}
    
    def set_template_data(self, data):
        """تعيين بيانات القالب من قاموس"""
        self.template_data = json.dumps(data)
    
    def get_participant_count(self):
        """الحصول على عدد المشاركين في المسابقة"""
        return self.participants.count()
    
    def is_full(self):
        """التحقق مما إذا كانت المسابقة ممتلئة"""
        if self.max_participants == 0:
            return False
        return self.get_participant_count() >= self.max_participants
    
    def __repr__(self):
        return f'<Contest {self.title}>'
