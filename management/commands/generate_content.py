from django.core.management.base import BaseCommand
from apps.exercises.generator import ExerciseGenerator, EvaluationGenerator, FlashcardGenerator
from apps.courses.models import Course, Lesson

class Command(BaseCommand):
    help = 'Genera contenido automático para cursos'
    
    def handle(self, *args, **options):
        self.stdout.write("Generando contenido automático...")
        
        # Crear curso de ejemplo
        course, created = Course.objects.get_or_create(
            title="Lingüística General",
            defaults={
                'description': "Curso completo de lingüística general con ejercicios automáticos",
                'is_published': True
            }
        )
        
        # Crear lecciones
        lessons_data = [
            {'title': 'Introducción a la Lingüística', 'order': 1},
            {'title': 'Nivel Fonológico', 'order': 2},
            {'title': 'Nivel Morfológico', 'order': 3},
            {'title': 'Nivel Sintáctico', 'order': 4},
            {'title': 'Nivel Semántico', 'order': 5},
        ]
        
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                course=course,
                title=lesson_data['title'],
                defaults={'order': lesson_data['order']}
            )
            
            # Generar ejercicios
            exercises = ExerciseGenerator.generate_multiple_choice(
                lesson_data['title'].lower().split()[1] if len(lesson_data['title'].split()) > 1 else 'general',
                'easy'
            )
            
            for ex in exercises:
                lesson.exercises.get_or_create(
                    title=ex['question'][:100],
                    defaults={
                        'type': 'multiple_choice',
                        'data': ex,
                        'points': 10
                    }
                )
            
            self.stdout.write(f"✓ Contenido generado para: {lesson.title}")
        
        # Generar 60 flashcards
        flashcards_json = FlashcardGenerator.generate_flashcards_json(course.title, 60)
        
        # Guardar JSON
        with open('flashcards_generated.json', 'w', encoding='utf-8') as f:
            f.write(flashcards_json)
        
        self.stdout.write(self.style.SUCCESS(f"✅ Contenido generado exitosamente!"))
