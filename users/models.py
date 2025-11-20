from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone as tz

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('pastor', 'Pastor'),
        ('elder', 'Elder'),
        ('deacon', 'Deacon'),
    ]
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(max_length=20, default='member', choices=ROLE_CHOICES)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    # If you want to use email as the username
    email = models.EmailField(unique=True)
    
    # Remove the username field and use email instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is still required by AbstractUser
    
    last_activity = models.DateTimeField(default=tz.now)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name of the user"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email
        
    def update_activity(self):
        """Update the last_activity field"""
        self.last_activity = tz.now()
        self.save(update_fields=['last_activity'])

class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def is_expired(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).days > 1