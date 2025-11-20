from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def update_last_activity(sender, instance, **kwargs):
    """
    Update last_activity field whenever user saves their profile
    """
    if hasattr(instance, 'last_activity'):
        instance.last_activity = timezone.now()
        instance.save(update_fields=['last_activity'])