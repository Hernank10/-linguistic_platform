from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_home(request):
    user = request.user
    context = {
        'user': user,
        'recent_courses': user.course_enrollments.all()[:5] if hasattr(user, 'course_enrollments') else [],
        'total_points': user.points,
        'completed_exercises': user.useranswer_set.count(),
        'mastered_flashcards': user.userflashcardprogress_set.filter(mastered=True).count(),
    }
    
    if user.role == 'teacher':
        context['courses_teaching'] = user.course_set.all()
        context['total_students'] = sum(c.enrollments.count() for c in user.course_set.all())
        context['pending_evaluations'] = 0  # Implementar lógica
    
    return render(request, 'dashboard/home.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user, course=course
    )
    
    lessons = course.lessons.all()
    completed_count = user_progress.completed_lessons.count()
    total_count = lessons.count()
    progress_percentage = (completed_count / total_count * 100) if total_count > 0 else 0
    
    context = {
        'course': course,
        'lessons': lessons,
        'progress': progress_percentage,
        'completed_count': completed_count,
        'total_count': total_count,
    }
    return render(request, 'dashboard/course_detail.html', context)

@login_required
def lesson_detail(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    user_progress = UserProgress.objects.get(user=request.user, course_id=course_id)
    
    is_completed = lesson in user_progress.completed_lessons.all()
    
    context = {
        'lesson': lesson,
        'is_completed': is_completed,
        'exercises': lesson.exercises.all(),
        'evaluations': lesson.evaluations.all(),
        'flashcard_sets': lesson.course.flashcard_sets.all(),
        'readings': lesson.readings.all(),
    }
    return render(request, 'dashboard/lesson_detail.html', context)

@login_required
def take_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    
    if request.method == 'POST':
        score = 0
        total_points = 0
        
        for question in evaluation.questions.all():
            total_points += question.points
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                selected_answer = Answer.objects.get(id=answer_id)
                is_correct = selected_answer.is_correct
                if is_correct:
                    score += question.points
                
                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    answer=selected_answer,
                    is_correct=is_correct
                )
        
        final_score = (score / total_points) * 100 if total_points > 0 else 0
        
        return render(request, 'dashboard/evaluation_result.html', {
            'evaluation': evaluation,
            'score': final_score,
            'passed': final_score >= evaluation.passing_score
        })
    
    context = {
        'evaluation': evaluation,
        'questions': evaluation.questions.all().prefetch_related('answers'),
    }
    return render(request, 'dashboard/take_evaluation.html', context)

@staff_member_required
def admin_create_course(request):
    """Vista para profesores crear cursos"""
    if request.method == 'POST':
        # Lógica para crear curso
        pass
    return render(request, 'dashboard/admin/create_course.html')
