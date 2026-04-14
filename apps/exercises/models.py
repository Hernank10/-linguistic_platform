from django.db import models
from apps.courses.models import Lesson
class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    question = models.TextField()
    correct_answer = models.CharField(max_length=500)
    points = models.IntegerField(default=10)
    def __str__(self): return self.title
