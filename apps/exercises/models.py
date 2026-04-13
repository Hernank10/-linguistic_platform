from django.db import models
from apps.courses.models import Lesson
import json

class Exercise(models.Model):
    TYPE_CHOICES = (
        ('multiple_choice', 'Opción Múltiple'),
        ('fill_blank', 'Completar'),
        ('matching', 'Emparejar'),
        ('true_false', 'Verdadero/Falso'),
    )
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    data = models.JSONField(default=dict)
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Evaluation(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='evaluations')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit_minutes = models.IntegerField(default=30)
    passing_score = models.IntegerField(default=70)
    
    def __str__(self):
        return f"Evaluación: {self.title}"

class Question(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.IntegerField(default=5)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.text[:50]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text[:50]

class UserAnswer(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
