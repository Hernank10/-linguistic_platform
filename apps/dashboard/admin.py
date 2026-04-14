from django.contrib import admin
from .models import UserProgress
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin): list_display = ('user', 'total_points', 'updated_at')
