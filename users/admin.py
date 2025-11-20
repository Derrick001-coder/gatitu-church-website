from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from .models import CustomUser, PasswordResetToken

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone', 'role', 'is_staff', 'is_active', 'last_activity', 'date_joined', 'user_actions']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined', 'last_activity']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Church Information', {
            'fields': ('phone', 'role', 'avatar')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Church Information', {
            'fields': ('phone', 'role', 'avatar')
        }),
    )
    
    # Add actions for bulk operations
    actions = ['activate_users', 'deactivate_users', 'delete_users']
    
    def user_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Delete</a>',
            f'{obj.pk}/delete/'
        )
    user_actions.short_description = 'Actions'
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def delete_users(self, request, queryset):
        # Soft delete - set is_active to False instead of actually deleting
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated (soft delete).')
    delete_users.short_description = "Delete selected users (Deactivate)"
    
    # Allow actual deletion for superusers
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.user_delete_view), name='auth_user_delete'),
        ]
        return custom_urls + urls
    
    def user_delete_view(self, request, object_id):
        # Only allow superusers to actually delete users
        if request.user.is_superuser:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(pk=object_id)
            user.delete()
            self.message_user(request, f'User {user.email} has been permanently deleted.')
        else:
            self.message_user(request, 'You do not have permission to permanently delete users.', level='ERROR')
        
        return HttpResponseRedirect('../../')
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'used', 'is_expired']
    list_filter = ['used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'