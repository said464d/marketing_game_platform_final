// ملف JavaScript الرئيسي للمنصة

// دالة للتحقق من صحة نموذج المشاركة
function validateParticipationForm() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    
    if (!name || name.length < 3) {
        alert('يرجى إدخال اسم صحيح (3 أحرف على الأقل)');
        return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('يرجى إدخال بريد إلكتروني صحيح');
        return false;
    }
    
    return true;
}

// دالة لإضافة حقول أسئلة جديدة في نموذج إنشاء المسابقة
function addQuestionField() {
    const questionsContainer = document.getElementById('questions-container');
    const questionCount = document.querySelectorAll('.question-item').length + 1;
    
    const questionHtml = `
        <div class="question-item card mb-3 p-3">
            <h5>السؤال ${questionCount}</h5>
            <div class="mb-3">
                <label for="question_${questionCount}" class="form-label">نص السؤال</label>
                <input type="text" class="form-control" id="question_${questionCount}" name="question_${questionCount}" required>
            </div>
            <div class="mb-3">
                <label class="form-label">الخيارات</label>
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionCount}" value="0" required>
                            </div>
                            <input type="text" class="form-control" name="option_${questionCount}_1" placeholder="الخيار 1" required>
                        </div>
                    </div>
                    <div class="col-md-6 mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionCount}" value="1" required>
                            </div>
                            <input type="text" class="form-control" name="option_${questionCount}_2" placeholder="الخيار 2" required>
                        </div>
                    </div>
                    <div class="col-md-6 mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionCount}" value="2" required>
                            </div>
                            <input type="text" class="form-control" name="option_${questionCount}_3" placeholder="الخيار 3" required>
                        </div>
                    </div>
                    <div class="col-md-6 mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionCount}" value="3" required>
                            </div>
                            <input type="text" class="form-control" name="option_${questionCount}_4" placeholder="الخيار 4" required>
                        </div>
                    </div>
                </div>
            </div>
            <button type="button" class="btn btn-sm btn-danger align-self-end" onclick="removeQuestion(this)">حذف السؤال</button>
        </div>
    `;
    
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = questionHtml;
    questionsContainer.appendChild(tempDiv.firstElementChild);
    
    // تحديث عدد الأسئلة في النموذج
    document.getElementById('question_count').value = questionCount;
}

// دالة لحذف سؤال من نموذج إنشاء المسابقة
function removeQuestion(button) {
    const questionItem = button.closest('.question-item');
    questionItem.remove();
    
    // إعادة ترقيم الأسئلة
    const questions = document.querySelectorAll('.question-item');
    questions.forEach((question, index) => {
        question.querySelector('h5').textContent = `السؤال ${index + 1}`;
    });
    
    // تحديث عدد الأسئلة في النموذج
    document.getElementById('question_count').value = questions.length;
}

// دالة لعرض معاينة المسابقة
function previewContest() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    
    if (!title || !description) {
        alert('يرجى إدخال عنوان ووصف المسابقة أولاً');
        return;
    }
    
    const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
    
    document.getElementById('preview-title').textContent = title;
    document.getElementById('preview-description').textContent = description;
    
    previewModal.show();
}

// دالة لمشاركة المسابقة على وسائل التواصل الاجتماعي
function shareContest(platform, url, title) {
    let shareUrl;
    
    switch (platform) {
        case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
            break;
        case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
            break;
        case 'whatsapp':
            shareUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(title + ' ' + url)}`;
            break;
        case 'linkedin':
            shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
            break;
    }
    
    if (shareUrl) {
        window.open(shareUrl, '_blank', 'width=600,height=400');
    }
}

// دالة لتحديث الوقت المتبقي للمسابقة
function updateCountdown(endDate, elementId) {
    const countdownElement = document.getElementById(elementId);
    if (!countdownElement) return;
    
    const endDateTime = new Date(endDate).getTime();
    
    const countdownInterval = setInterval(function() {
        const now = new Date().getTime();
        const distance = endDateTime - now;
        
        if (distance < 0) {
            clearInterval(countdownInterval);
            countdownElement.innerHTML = "انتهت المسابقة";
            return;
        }
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        countdownElement.innerHTML = `${days} يوم ${hours} ساعة ${minutes} دقيقة ${seconds} ثانية`;
    }, 1000);
}

// تهيئة الصفحة عند تحميلها
document.addEventListener('DOMContentLoaded', function() {
    // تهيئة نماذج التحقق
    const participationForm = document.getElementById('participation-form');
    if (participationForm) {
        participationForm.addEventListener('submit', function(event) {
            if (!validateParticipationForm()) {
                event.preventDefault();
            }
        });
    }
    
    // تهيئة أزرار إضافة الأسئلة
    const addQuestionButton = document.getElementById('add-question-btn');
    if (addQuestionButton) {
        addQuestionButton.addEventListener('click', addQuestionField);
        // إضافة سؤال افتراضي عند تحميل الصفحة
        addQuestionField();
    }
    
    // تهيئة زر المعاينة
    const previewButton = document.getElementById('preview-btn');
    if (previewButton) {
        previewButton.addEventListener('click', previewContest);
    }
    
    // تهيئة العد التنازلي للمسابقات
    const countdownElements = document.querySelectorAll('[data-countdown]');
    countdownElements.forEach(function(element) {
        const endDate = element.getAttribute('data-countdown');
        updateCountdown(endDate, element.id);
    });
});
