from django.core.management.base import BaseCommand
from apps.exercises.models import Exercise
from apps.flashcards.models import Flashcard, FlashcardSet
import json

class Command(BaseCommand):
    help = 'Carga datos desde archivos JSON'
    
    def add_arguments(self, parser):
        parser.add_argument('--exercises', type=str, help='Archivo JSON de ejercicios')
        parser.add_argument('--flashcards', type=str, help='Archivo JSON de flashcards')
    
    def handle(self, *args, **options):
        if options['exercises']:
            with open(options['exercises'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ex_data in data['exercises']:
                    exercise, created = Exercise.objects.get_or_create(
                        title=ex_data['question'][:100],
                        defaults={
                            'type': ex_data['type'],
                            'data': ex_data,
                            'points': 10
                        }
                    )
                    self.stdout.write(f"{'✓ Creado' if created else '✓ Actualizado'}: {exercise.title[:50]}")
        
        if options['flashcards']:
            flashcard_set, _ = FlashcardSet.objects.get_or_create(
                title="Curso Completo de Lingüística",
                defaults={'description': "60 flashcards para dominar conceptos clave"}
            )
            
            with open(options['flashcards'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                for card_data in data['flashcards']:
                    flashcard, created = Flashcard.objects.get_or_create(
                        flashcard_set=flashcard_set,
                        term=card_data['term'],
                        defaults={
                            'definition': card_data['definition'],
                            'example': card_data.get('example', '')
                        }
                    )
                    self.stdout.write(f"{'✓ Creada' if created else '✓ Actualizada'}: {flashcard.term}")
