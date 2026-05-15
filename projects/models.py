from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='assigned_projects',
        blank=True
    )

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_teams'
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teams',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name