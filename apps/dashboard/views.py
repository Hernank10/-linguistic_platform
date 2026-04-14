from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def dashboard_home(request):
    """Página principal del dashboard"""
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def course_detail(request, course_id):
    """Detalle de un curso"""
    context = {
        'course_id': course_id,
    }
    return render(request, 'dashboard/course_detail.html', context)

@login_required
def lesson_detail(request, course_id, lesson_id):
    """Detalle de una lección"""
    context = {
        'course_id': course_id,
        'lesson_id': lesson_id,
    }
    return render(request, 'dashboard/lesson_detail.html', context)

@login_required
def complete_lesson(request, lesson_id):
    """Marcar una lección como completada"""
    # Aquí iría la lógica para marcar la lección como completada
    from django.shortcuts import redirect
    from django.contrib import messages
    messages.success(request, f'Lección {lesson_id} completada!')
    return redirect('dashboard:home')

@login_required
def take_evaluation(request, evaluation_id):
    """Tomar una evaluación"""
    context = {
        'evaluation_id': evaluation_id,
    }
    return render(request, 'dashboard/take_evaluation.html', context)

@staff_member_required
def admin_create_course(request):
    """Vista para profesores crear cursos"""
    from django.shortcuts import render
    return render(request, 'dashboard/admin_create_course.html')
