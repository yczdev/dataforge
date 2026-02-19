from django.db import models
from django.contrib.auth.models import User

class Schema(models.Model):
    owner = models.ForeignKey(User, related_name='schemas', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    definition = models.JSONField(default=list)
    row_count = models.PositiveIntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} by {self.owner.username}"
