from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import CustomUser


# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new announcement
        super().save(*args, **kwargs)
        
        # Create notification for new announcements
        if is_new and self.is_active:
            self.create_notification()

    def create_notification(self):
        # Create notifications for all users except the author
        try:
            # Create notifications for all active users except the author
            users = CustomUser.objects.filter(is_active=True).exclude(id=self.author.id)
            for user in users:
                Notification.objects.create(
                    user=user,
                    title='📢 New Announcement',
                    message=f'{self.author.get_full_name()} posted: {self.title}',
                    notification_type='announcement'
                )
            print(f"Created notifications for {users.count()} users")  # Debug
        except Exception as e:
            print(f"Error creating announcement notifications: {e}")

    
    def __str__(self):
        return self.title

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('ongoing', 'Ongoing'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Create notification for new activities
        if is_new:
            self.create_notification()

    def create_notification(self):
        try:
            users = CustomUser.objects.filter(is_active=True)
            activity_type_display = self.get_activity_type_display()
            
            for user in users:
                Notification.objects.create(
                    user=user,
                    title='📅 New Activity',
                    message=f'New {activity_type_display.lower()}: {self.title}',
                    notification_type='activity'
                )
            print(f"Created activity notifications for {users.count()} users")  # Debug
        except Exception as e:
            print(f"Error creating activity notifications: {e}")
    
    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Create notification for new blog posts
        if is_new:
            self.create_notification()

    def create_notification(self):
        try:
            users = CustomUser.objects.filter(is_active=True).exclude(id=self.author.id)
            for user in users:
                Notification.objects.create(
                    user=user,
                    title='📝 New Blog Post',
                    message=f'{self.author.get_full_name()} published: {self.title}',
                    notification_type='blog'
                )
            print(f"Created blog notifications for {users.count()} users")  # Debug
        except Exception as e:
            print(f"Error creating blog notifications: {e}")
    
    def __str__(self):
        return self.title
    
    

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}: {self.message[:50]}"

class Photo(models.Model):
    PHOTO_TYPES = [
        ('church', 'Church Photo'),
        ('trip', 'Trip Photo'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPES)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class FinancialRecord(models.Model):
    offering = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    donations = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    record_date = models.DateField(auto_now_add=True)
    
    @property
    def available_funds(self):
        return self.offering + self.donations - self.expenses
    
    def __str__(self):
        return f"Financial Record - {self.record_date}"
    
    class Meta:
        ordering = ['-record_date']
    
    
class NotificationManager(models.Manager):
    def unread(self):
        return self.filter(is_read=False)
    
    def read(self):
        return self.filter(is_read=True)
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    notification_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = NotificationManager()
    
    def __str__(self):
        return f"{self.title} - {self.user.email if self.user else 'All Users'}"
    
    class Meta:
        ordering = ['-created_at']
        
        
    @receiver(post_save, sender=FinancialRecord)
    def create_financial_notification(sender, instance, created, **kwargs):
        """
        Create notifications when new financial records are added
        Only create notifications for significant updates (not every small change)
        """
        if created:
            try:
                # Only notify if the amounts are significant (more than 1000 KSh)
                total_amount = instance.offering + instance.donations
                if total_amount > 1000:
                    users = CustomUser.objects.filter(is_active=True)
                    for user in users:
                        Notification.objects.create(
                            user=user,
                            title='💰 Financial Update',
                            message=f'New financial records updated: Offering KSh {instance.offering:,}, Donations KSh {instance.donations:,}',
                            notification_type='financial'
                        )
                    print(f"Created financial notifications for {users.count()} users")
            except Exception as e:
                print(f"Error creating financial notifications: {e}")

    # Signals for other models
    @receiver(post_save, sender=Announcement)
    def create_announcement_notification(sender, instance, created, **kwargs):
        """Create notifications when new announcements are posted"""
        if created and instance.is_active:
            try:
                users = CustomUser.objects.filter(is_active=True).exclude(id=instance.author.id)
                for user in users:
                    Notification.objects.create(
                        user=user,
                        title='📢 New Announcement',
                        message=f'{instance.author.get_full_name()} posted: {instance.title}',
                        notification_type='announcement'
                    )
                print(f"Created announcement notifications for {users.count()} users")
            except Exception as e:
                print(f"Error creating announcement notifications: {e}")

    @receiver(post_save, sender=Activity)
    def create_activity_notification(sender, instance, created, **kwargs):
        """Create notifications when new activities are added"""
        if created:
            try:
                users = CustomUser.objects.filter(is_active=True)
                activity_type_display = instance.get_activity_type_display()
                
                for user in users:
                    Notification.objects.create(
                        user=user,
                        title='📅 New Activity',
                        message=f'New {activity_type_display.lower()}: {instance.title}',
                        notification_type='activity'
                    )
                print(f"Created activity notifications for {users.count()} users")
            except Exception as e:
                print(f"Error creating activity notifications: {e}")

    @receiver(post_save, sender=BlogPost)
    def create_blog_notification(sender, instance, created, **kwargs):
        """Create notifications when new blog posts are published"""
        if created:
            try:
                users = CustomUser.objects.filter(is_active=True).exclude(id=instance.author.id)
                for user in users:
                    Notification.objects.create(
                        user=user,
                        title='📝 New Blog Post',
                        message=f'{instance.author.get_full_name()} published: {instance.title}',
                        notification_type='blog'
                    )
                print(f"Created blog notifications for {users.count()} users")
            except Exception as e:
                print(f"Error creating blog notifications: {e}")
        
        def __str__(self):
            return self.title
