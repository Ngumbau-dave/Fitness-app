from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ACTIVITY_CHOICES = [
    ('RUN', 'Running'),
    ('CYC', 'Cycling'),
    ('SWM', 'Swimming'),
    ('GYM', 'Gym'),
    ('YOG', 'Yoga'),
    ('OTH', 'Other'),
]

# MET values for calorie calculation
MET_VALUES = {
    'RUN': 10.0,
    'CYC': 8.0,
    'SWM': 10.0,
    'GYM': 6.0,
    'YOG': 3.0,
    'OTH': 5.0,
}

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, default='OTH')
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    calories_burned = models.PositiveIntegerField(null=True, blank=True, editable=False)  # Auto-calculated
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.duration:
            met = MET_VALUES.get(self.activity_type, 5.0)
            weight_kg = 70  # Default weight — customize later
            hours = self.duration / 60
            self.calories_burned = int(met * weight_kg * hours)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-date']
        # Add this at the end of models.py
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Automatically create a Profile when a User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save profile when User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()