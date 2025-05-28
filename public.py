from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.models.contest import Contest
from src.models.participant import Participant
from src.main import db
import json

public_bp = Blueprint('public', __name__)

@public_bp.route('/contests')
def contests():
    """عرض جميع المسابقات النشطة"""
    active_contests = Contest.query.filter_by(is_active=True).all()
    return render_template('public/contests.html', contests=active_contests)

@public_bp.route('/contests/<int:contest_id>')
def view_contest(contest_id):
    """عرض تفاصيل المسابقة للمشاركين"""
    contest = Contest.query.get_or_404(contest_id)
    
    if not contest.is_active:
        flash('هذه المسابقة غير متاحة حالياً.')
        return redirect(url_for('public.contests'))
    
    return render_template('public/contest_details.html', contest=contest)

@public_bp.route('/contests/<int:contest_id>/participate', methods=['GET', 'POST'])
def participate(contest_id):
    """المشاركة في المسابقة"""
    contest = Contest.query.get_or_404(contest_id)
    
    if not contest.is_active:
        flash('هذه المسابقة غير متاحة حالياً.')
        return redirect(url_for('public.contests'))
    
    if contest.is_full():
        flash('عذراً، هذه المسابقة ممتلئة بالفعل.')
        return redirect(url_for('public.view_contest', contest_id=contest.id))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # التحقق من عدم وجود مشارك بنفس البريد الإلكتروني
        existing_participant = Participant.query.filter_by(email=email, contest_id=contest.id).first()
        if existing_participant:
            flash('لقد شاركت بالفعل في هذه المسابقة.')
            return redirect(url_for('public.view_contest', contest_id=contest.id))
        
        participant = Participant(
            name=name,
            email=email,
            phone=phone,
            contest_id=contest.id,
            ip_address=request.remote_addr
        )
        
        db.session.add(participant)
        db.session.commit()
        
        return redirect(url_for('public.contest_play', contest_id=contest.id, participant_id=participant.id))
    
    return render_template('public/participate_form.html', contest=contest)

@public_bp.route('/contests/<int:contest_id>/play/<int:participant_id>', methods=['GET', 'POST'])
def contest_play(contest_id, participant_id):
    """صفحة اللعب في المسابقة"""
    contest = Contest.query.get_or_404(contest_id)
    participant = Participant.query.get_or_404(participant_id)
    
    if participant.contest_id != contest.id:
        flash('بيانات غير صحيحة.')
        return redirect(url_for('public.contests'))
    
    if participant.completed:
        return redirect(url_for('public.contest_result', contest_id=contest.id, participant_id=participant.id))
    
    template_data = contest.get_template_data()
    
    if request.method == 'POST':
        answers = {}
        score = 0
        
        if contest.contest_type == 'quiz':
            for i, question in enumerate(template_data.get('questions', [])):
                answer = request.form.get(f'answer_{i}')
                answers[f'question_{i}'] = answer
                
                if answer and int(answer) == question.get('correct'):
                    score += 1
        
        participant.answers = json.dumps(answers)
        participant.score = score
        participant.completed = True
        db.session.commit()
        
        return redirect(url_for('public.contest_result', contest_id=contest.id, participant_id=participant.id))
    
    return render_template('public/contest_play.html', contest=contest, participant=participant, template_data=template_data)

@public_bp.route('/contests/<int:contest_id>/result/<int:participant_id>')
def contest_result(contest_id, participant_id):
    """عرض نتيجة المشاركة"""
    contest = Contest.query.get_or_404(contest_id)
    participant = Participant.query.get_or_404(participant_id)
    
    if participant.contest_id != contest.id:
        flash('بيانات غير صحيحة.')
        return redirect(url_for('public.contests'))
    
    if not participant.completed:
        flash('يجب إكمال المسابقة أولاً.')
        return redirect(url_for('public.contest_play', contest_id=contest.id, participant_id=participant.id))
    
    # حساب ترتيب المشارك
    participants = contest.participants.filter_by(completed=True).order_by(Participant.score.desc()).all()
    rank = next((i + 1 for i, p in enumerate(participants) if p.id == participant.id), 0)
    
    return render_template('public/contest_result.html', contest=contest, participant=participant, rank=rank, total=len(participants))
