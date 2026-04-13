from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Estudiante'),
        ('teacher', 'Profesor'),
        ('admin', 'Administrador'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    # Corregir conflictos con auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='linguistic_user_set',  # Nombre único
        related_query_name='linguistic_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='linguistic_user_set',  # Nombre único
        related_query_name='linguistic_user',
    )
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
