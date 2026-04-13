from django.contrib import admin
from django import forms
from .models import Course, Lesson, ReadingMaterial
from apps.exercises.generator import ExerciseGenerator, EvaluationGenerator, FlashcardGenerator
from django.http import JsonResponse, HttpResponse
from django.urls import path
import json

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'description']
    actions = ['publish_courses', 'generate_flashcards']
    
    def publish_courses(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} cursos publicados")
    publish_courses.short_description = "Publicar cursos seleccionados"
    
    def generate_flashcards(self, request, queryset):
        for course in queryset:
            flashcards_json = FlashcardGenerator.generate_flashcards_json(course.title, 60)
            # Guardar en archivo o modelo
            self.message_user(request, f"Flashcards generados para {course.title}")
    generate_flashcards.short_description = "Generar 60 flashcards para cursos"

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes']
    list_editable = ['order', 'duration_minutes']
    actions = ['generate_exercises', 'generate_evaluation']
    
    def generate_exercises(self, request, queryset):
        for lesson in queryset:
            exercises = ExerciseGenerator.generate_multiple_choice('semantico', 'medium')
            for ex in exercises:
                lesson.exercises.create(
                    title=f"Ejercicio: {ex['question'][:50]}",
                    type='multiple_choice',
                    data=ex
                )
        self.message_user(request, f"Ejercicios generados para {queryset.count()} lecciones")
    generate_exercises.short_description = "Generar ejercicios automáticos"
    
    def generate_evaluation(self, request, queryset):
        for lesson in queryset:
            evaluation_json = EvaluationGenerator.generate_evaluation_json(lesson.title, 10)
            lesson.evaluations.create(
                title=f"Evaluación: {lesson.title}",
                description="Evaluación automática generada",
                time_limit_minutes=30,
                passing_score=70
            )
        self.message_user(request, f"Evaluaciones generadas para {queryset.count()} lecciones")
    generate_evaluation.short_description = "Generar evaluación automática"

@admin.register(ReadingMaterial)
class ReadingMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson']
    fields = ['title', 'content', 'html_template']
