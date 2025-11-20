from django.contrib import admin
from .models import Announcement, Activity, BlogPost, Comment, ChatMessage, Photo, FinancialRecord, Notification

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date', 'is_active']
    list_filter = ['date', 'is_active']
    search_fields = ['title', 'content']
    list_editable = ['is_active']
    date_hierarchy = 'date'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'date', 'created_at']
    list_filter = ['activity_type', 'date']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date']
    list_filter = ['date']
    search_fields = ['title', 'content']
    date_hierarchy = 'date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'date']
    list_filter = ['date']
    search_fields = ['content', 'author__email']
    date_hierarchy = 'date'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['message', 'user__email']
    date_hierarchy = 'timestamp'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo_type', 'upload_date']
    list_filter = ['photo_type', 'upload_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'upload_date'

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ['offering', 'donations', 'expenses', 'available_funds', 'record_date']
    list_filter = ['record_date']
    date_hierarchy = 'record_date'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__email']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'