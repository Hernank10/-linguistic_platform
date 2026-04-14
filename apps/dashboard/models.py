from django.db import models
from django.conf import settings
class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    total_points = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.user.username} - {self.total_points}"
