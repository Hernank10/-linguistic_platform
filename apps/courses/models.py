from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    content = models.TextField(help_text="Contenido HTML de la lección")
    video_url = models.URLField(blank=True)
    duration_minutes = models.IntegerField(default=30)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class ReadingMaterial(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='readings')
    title = models.CharField(max_length=200)
    content = models.TextField()
    html_template = models.TextField(blank=True, help_text="Plantilla HTML personalizada")
    
    def save(self, *args, **kwargs):
        if not self.html_template:
            self.html_template = f"""
            <div class="reading-material">
                <h2>{self.title}</h2>
                <div class="content">{self.content}</div>
            </div>
            """
        super().save(*args, **kwargs)
