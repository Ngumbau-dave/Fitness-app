from django.db import models
from django.contrib.auth.models import get_user_model

User = get_user_model()

class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('RUN', 'Running'),
        ('CYC', 'Cycling'),
        ('SWM', 'Swimming'),
        ('GYM', 'Gym'),
        ('YOG', 'Yoga'),
    
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    calories_burned = models.PositiveIntegerField(null=True,blank=True))
    date=models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type} on {self.date}"

# Create your models here.
