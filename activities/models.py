from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    title = models.CharField(max_length=255, unique=True)
    points = models.IntegerField()


class Submission(models.Model):
    grade = models.IntegerField(default=None, blank=True, null=True)
    repo = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="submissions", on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="submissions") 
