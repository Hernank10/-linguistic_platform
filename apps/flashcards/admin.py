from django.contrib import admin
from .models import FlashcardSet, Flashcard
@admin.register(FlashcardSet)
class FlashcardSetAdmin(admin.ModelAdmin): list_display = ('title', 'created_at')
@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin): list_display = ('term', 'flashcard_set')
