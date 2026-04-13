from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class FlashcardLevel(models.Model):
    """Nivel de flashcards según MCER"""
    LEVEL_CHOICES = [
        ('A1', 'Principiante'),
        ('A2', 'Básico'),
        ('B1', 'Intermedio'),
        ('B2', 'Intermedio Alto'),
        ('C1', 'Avanzado'),
    ]
    
    code = models.CharField(max_length=2, choices=LEVEL_CHOICES, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    total_cards = models.IntegerField(default=20)
    points_per_card = models.IntegerField(default=5)
    daily_goal = models.IntegerField(default=5)
    passing_score = models.IntegerField(default=70)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Flashcard(models.Model):
    """Flashcard individual"""
    level = models.ForeignKey(FlashcardLevel, on_delete=models.CASCADE, related_name='flashcards')
    term = models.CharField(max_length=200)
    definition = models.TextField()
    example = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    points = models.IntegerField(default=5)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['level__order', 'order']
    
    def __str__(self):
        return f"[{self.level.code}] {self.term}"

class StudentFlashcardProgress(models.Model):
    """Progreso del estudiante en cada flashcard"""
    MASTERY_LEVELS = [
        (0, 'No vista'),
        (1, 'En progreso'),
        (2, 'En revisión'),
        (3, 'Semidominada'),
        (4, 'Dominada'),
        (5, 'Maestría'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_progress')
    flashcard = models.ForeignKey('Flashcard', on_delete=models.CASCADE, related_name='student_progress')
    mastery_level = models.IntegerField(choices=MASTERY_LEVELS, default=0)
    times_reviewed = models.IntegerField(default=0)
    correct_reviews = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(default=timezone.now)
    is_mastered = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'flashcard']
    
    def __str__(self):
        return f"{self.student.username} - {self.flashcard.term}"
