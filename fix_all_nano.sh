#!/bin/bash

echo "=== CORRIGIENDO TODOS LOS ARCHIVOS ==="

# Courses
cat > apps/courses/models.py << 'COURSES'
from django.db import models
from django.conf import settings
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    def __str__(self): return self.title
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    class Meta: ordering = ['order']
    def __str__(self): return f"{self.course.title} - {self.title}"
COURSES

cat > apps/courses/admin.py << 'CADMIN'
from django.contrib import admin
from .models import Course, Lesson
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin): list_display = ('title', 'created_at', 'is_published')
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin): list_display = ('title', 'course', 'order')
CADMIN

# Exercises
cat > apps/exercises/models.py << 'EXERCISES'
from django.db import models
from apps.courses.models import Lesson
class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    question = models.TextField()
    correct_answer = models.CharField(max_length=500)
    points = models.IntegerField(default=10)
    def __str__(self): return self.title
EXERCISES

cat > apps/exercises/admin.py << 'EADMIN'
from django.contrib import admin
from .models import Exercise
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin): list_display = ('title', 'lesson', 'points')
EADMIN

# Flashcards
cat > apps/flashcards/models.py << 'FLASHCARDS'
from django.db import models
class FlashcardSet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
class Flashcard(models.Model):
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name='flashcards')
    term = models.CharField(max_length=200)
    definition = models.TextField()
    example = models.TextField(blank=True)
    def __str__(self): return self.term
FLASHCARDS

cat > apps/flashcards/admin.py << 'FADMIN'
from django.contrib import admin
from .models import FlashcardSet, Flashcard
@admin.register(FlashcardSet)
class FlashcardSetAdmin(admin.ModelAdmin): list_display = ('title', 'created_at')
@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin): list_display = ('term', 'flashcard_set')
FADMIN

# Dashboard
cat > apps/dashboard/models.py << 'DASHBOARD'
from django.db import models
from django.conf import settings
class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    total_points = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.user.username} - {self.total_points}"
DASHBOARD

cat > apps/dashboard/admin.py << 'DADMIN'
from django.contrib import admin
from .models import UserProgress
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin): list_display = ('user', 'total_points', 'updated_at')
DADMIN

# Limpiar y migrar
rm -f db.sqlite3
for app in accounts courses exercises flashcards dashboard; do
    rm -rf apps/$app/migrations/*.py
    touch apps/$app/migrations/__init__.py
done

python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py makemigrations exercises
python manage.py makemigrations flashcards
python manage.py makemigrations dashboard
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@linguistic.com', 'admin123')
    print('✅ Superusuario: admin / admin123')
"

echo "✅ TODO CORREGIDO"
echo "Ejecuta: python manage.py runserver"
