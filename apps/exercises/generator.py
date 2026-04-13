import json
import random
from typing import List, Dict

class ExerciseGenerator:
    @staticmethod
    def generate_multiple_choice(topic: str, difficulty: str = 'medium') -> List[Dict]:
        """Genera ejercicios de opción múltiple automáticamente"""
        templates = {
            'semantico': {
                'easy': [
                    {
                        'question': '¿Cuál de las siguientes palabras es un SUSTANTIVO?',
                        'options': ['correr', 'casa', 'rápido', 'grande'],
                        'correct': 'casa'
                    },
                    {
                        'question': '¿Cuál es un ADJETIVO calificativo?',
                        'options': ['mesa', 'alto', 'comer', 'felizmente'],
                        'correct': 'alto'
                    }
                ],
                'medium': [
                    {
                        'question': 'Identifica la categoría gramatical de "rápidamente"',
                        'options': ['Adjetivo', 'Sustantivo', 'Adverbio', 'Verbo'],
                        'correct': 'Adverbio'
                    }
                ]
            },
            'morfologico': {
                'easy': [
                    {
                        'question': '¿Cuál es la raíz de la palabra "cantante"?',
                        'options': ['cant', 'ante', 'canta', 'nte'],
                        'correct': 'cant'
                    }
                ]
            },
            'fonologico': {
                'easy': [
                    {
                        'question': '¿Cuántos fonemas tiene la palabra "casa"?',
                        'options': ['2', '3', '4', '5'],
                        'correct': '4'
                    }
                ]
            }
        }
        
        return templates.get(topic, {}).get(difficulty, [])
    
    @staticmethod
    def generate_fill_blank(text: str) -> Dict:
        """Genera ejercicio de completar espacios en blanco"""
        words = text.split()
        blank_position = random.randint(0, len(words) - 1)
        correct_word = words[blank_position]
        words[blank_position] = "______"
        
        return {
            'text': ' '.join(words),
            'correct': correct_word,
            'options': [correct_word] + random.sample([w for w in words if w != correct_word], 3)
        }
    
    @staticmethod
    def generate_true_false(statement: str, is_true: bool) -> Dict:
        """Genera ejercicio de verdadero/falso"""
        return {
            'statement': statement,
            'is_true': is_true
        }

class EvaluationGenerator:
    @staticmethod
    def generate_evaluation_json(lesson_title: str, num_questions: int = 10) -> str:
        """Genera una evaluación completa en formato JSON"""
        evaluation = {
            'title': f'Evaluación: {lesson_title}',
            'description': 'Evaluación automática de conocimientos',
            'time_limit': 30,
            'passing_score': 70,
            'questions': []
        }
        
        question_templates = [
            {'text': '¿Qué estudia la semántica?', 'type': 'multiple_choice'},
            {'text': 'Define "morfema"', 'type': 'open'},
            {'text': 'La fonología estudia...', 'type': 'fill_blank'},
        ]
        
        for i in range(num_questions):
            template = random.choice(question_templates)
            evaluation['questions'].append({
                'id': i + 1,
                'text': template['text'],
                'type': template['type'],
                'points': 10
            })
        
        return json.dumps(evaluation, indent=2, ensure_ascii=False)

class FlashcardGenerator:
    @staticmethod
    def generate_flashcards_json(course_title: str, num_cards: int = 60) -> str:
        """Genera 60 flashcards en formato JSON"""
        linguistic_concepts = [
            {'term': 'Fonema', 'definition': 'Unidad mínima de sonido que puede distinguir significados', 
             'example': '/p/ y /b/ en "pala" vs "bala"'},
            {'term': 'Morfema', 'definition': 'Unidad mínima de significado', 
             'example': 'En "gatos": "gat" (lexema) + "o" (género) + "s" (número)'},
            {'term': 'Sintagma', 'definition': 'Grupo de palabras que cumple una función sintáctica', 
             'example': 'Sintagma nominal: "El perro grande"'},
            {'term': 'Oración', 'definition': 'Unidad de comunicación con sentido completo', 
             'example': 'Juan estudia lingüística.'},
            {'term': 'Sujeto', 'definition': 'Quien realiza la acción o de quien se dice algo', 
             'example': 'En "María canta", el sujeto es "María"'},
            {'term': 'Predicado', 'definition': 'Lo que se dice del sujeto', 
             'example': 'En "María canta", el predicado es "canta"'},
        ]
        
        flashcards = []
        for i in range(num_cards):
            concept = linguistic_concepts[i % len(linguistic_concepts)]
            flashcards.append({
                'id': i + 1,
                'term': concept['term'],
                'definition': concept['definition'],
                'example': concept['example'],
                'category': random.choice(['Fonología', 'Morfología', 'Sintaxis', 'Semántica'])
            })
        
        return json.dumps(flashcards, indent=2, ensure_ascii=False)
