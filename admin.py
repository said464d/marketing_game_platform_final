from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.models.contest import Contest
from src.models.company import Company
from src.main import db
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def index():
    """لوحة تحكم المدير"""
    if not current_user.company:
        return redirect(url_for('admin.create_company'))
    
    company = current_user.company
    contests = company.contests.all()
    
    return render_template('admin/index.html', company=company, contests=contests)

@admin_bp.route('/company', methods=['GET', 'POST'])
@login_required
def create_company():
    """إنشاء أو تعديل شركة"""
    company = current_user.company
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        website = request.form.get('website')
        
        if not company:
            company = Company(name=name, description=description, website=website, user_id=current_user.id)
            db.session.add(company)
            flash('تم إنشاء الشركة بنجاح!')
        else:
            company.name = name
            company.description = description
            company.website = website
            flash('تم تحديث معلومات الشركة بنجاح!')
        
        db.session.commit()
        return redirect(url_for('admin.index'))
    
    return render_template('admin/company_form.html', company=company)

@admin_bp.route('/contests/new', methods=['GET', 'POST'])
@login_required
def create_contest():
    """إنشاء مسابقة جديدة"""
    if not current_user.company:
        flash('يجب إنشاء شركة أولاً!')
        return redirect(url_for('admin.create_company'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        rules = request.form.get('rules')
        contest_type = request.form.get('contest_type')
        prize_description = request.form.get('prize_description')
        
        # إنشاء بيانات القالب حسب نوع المسابقة
        template_data = {}
        if contest_type == 'quiz':
            questions = []
            for i in range(1, int(request.form.get('question_count', 0)) + 1):
                question = {
                    'text': request.form.get(f'question_{i}'),
                    'options': [
                        request.form.get(f'option_{i}_1'),
                        request.form.get(f'option_{i}_2'),
                        request.form.get(f'option_{i}_3'),
                        request.form.get(f'option_{i}_4')
                    ],
                    'correct': int(request.form.get(f'correct_{i}', 0))
                }
                questions.append(question)
            template_data['questions'] = questions
        
        contest = Contest(
            title=title,
            description=description,
            rules=rules,
            contest_type=contest_type,
            prize_description=prize_description,
            company_id=current_user.company.id,
            template_data=json.dumps(template_data)
        )
        
        db.session.add(contest)
        db.session.commit()
        
        flash('تم إنشاء المسابقة بنجاح!')
        return redirect(url_for('admin.index'))
    
    return render_template('admin/contest_form.html')

@admin_bp.route('/contests/<int:contest_id>')
@login_required
def view_contest(contest_id):
    """عرض تفاصيل المسابقة"""
    contest = Contest.query.get_or_404(contest_id)
    
    if contest.company.user_id != current_user.id:
        flash('غير مصرح لك بالوصول إلى هذه المسابقة!')
        return redirect(url_for('admin.index'))
    
    participants = contest.participants.all()
    
    return render_template('admin/contest_details.html', contest=contest, participants=participants)

@admin_bp.route('/contests/<int:contest_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contest(contest_id):
    """تعديل المسابقة"""
    contest = Contest.query.get_or_404(contest_id)
    
    if contest.company.user_id != current_user.id:
        flash('غير مصرح لك بتعديل هذه المسابقة!')
        return redirect(url_for('admin.index'))
    
    if request.method == 'POST':
        contest.title = request.form.get('title')
        contest.description = request.form.get('description')
        contest.rules = request.form.get('rules')
        contest.prize_description = request.form.get('prize_description')
        contest.is_active = True if request.form.get('is_active') else False
        
        db.session.commit()
        
        flash('تم تحديث المسابقة بنجاح!')
        return redirect(url_for('admin.view_contest', contest_id=contest.id))
    
    return render_template('admin/contest_edit.html', contest=contest)

@admin_bp.route('/contests/<int:contest_id>/delete', methods=['POST'])
@login_required
def delete_contest(contest_id):
    """حذف المسابقة"""
    contest = Contest.query.get_or_404(contest_id)
    
    if contest.company.user_id != current_user.id:
        flash('غير مصرح لك بحذف هذه المسابقة!')
        return redirect(url_for('admin.index'))
    
    db.session.delete(contest)
    db.session.commit()
    
    flash('تم حذف المسابقة بنجاح!')
    return redirect(url_for('admin.index'))
