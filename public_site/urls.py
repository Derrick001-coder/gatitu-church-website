from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('announcements/', views.announcements, name='announcements'),
    path('activities/', views.activities, name='activities'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('community/', views.community_chat, name='community_chat'),
    path('community/send/', views.send_message, name='send_message'),
    path('financial/', views.financial_updates, name='financial_updates'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/count/', views.notification_count, name='notification_count'),
]