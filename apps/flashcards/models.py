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
