from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.models.contest import Contest
from src.models.participant import Participant
from src.main import db

contests_bp = Blueprint('contests', __name__, url_prefix='/contests')

@contests_bp.route('/<int:contest_id>/leaderboard')
def leaderboard(contest_id):
    """عرض لوحة المتصدرين للمسابقة"""
    contest = Contest.query.get_or_404(contest_id)
    
    # الحصول على المشاركين الذين أكملوا المسابقة مرتبين حسب النقاط
    participants = contest.participants.filter_by(completed=True).order_by(Participant.score.desc()).all()
    
    return render_template('contests/leaderboard.html', contest=contest, participants=participants)

@contests_bp.route('/<int:contest_id>/share')
def share(contest_id):
    """صفحة مشاركة المسابقة على وسائل التواصل الاجتماعي"""
    contest = Contest.query.get_or_404(contest_id)
    
    # إنشاء روابط المشاركة
    share_url = request.host_url + url_for('public.view_contest', contest_id=contest.id)
    
    return render_template('contests/share.html', contest=contest, share_url=share_url)
