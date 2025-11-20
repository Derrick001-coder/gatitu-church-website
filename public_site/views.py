from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Announcement, Activity, BlogPost, Comment, ChatMessage, Photo, FinancialRecord
from .models import Notification


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})

@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read for the current user"""
    try:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def notification_count(request):
    """Get unread notification count"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})

def home(request):
    announcements = Announcement.objects.filter(is_active=True).order_by('-date')[:5]
    activities = Activity.objects.all().order_by('-date')[:6]
    latest_financial = FinancialRecord.objects.order_by('-record_date').first()
    church_photos = Photo.objects.filter(photo_type='church')[:8]
    trip_photos = Photo.objects.filter(photo_type='trip')[:8]
    
    context = {
        'announcements': announcements,
        'activities': activities,
        'financial': latest_financial,
        'church_photos': church_photos,
        'trip_photos': trip_photos,
    }
    return render(request, 'public_site/home.html', context)

def gallery(request):
    church_photos = Photo.objects.filter(photo_type='church')
    trip_photos = Photo.objects.filter(photo_type='trip')
    
    context = {
        'church_photos': church_photos,
        'trip_photos': trip_photos,
    }
    return render(request, 'public_site/gallery.html', context)

def announcements(request):
    announcements = Announcement.objects.filter(is_active=True).order_by('-date')
    return render(request, 'public_site/announcements.html', {'announcements': announcements})

def activities(request):
    activities = Activity.objects.all().order_by('-date')
    return render(request, 'public_site/activities.html', {'activities': activities})

@login_required
def blog(request):
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'public_site/blog.html', {'posts': posts})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, id=post_id)
        content = request.POST.get('content')
        
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
        return redirect('blog')

@login_required
def community_chat(request):
    messages = ChatMessage.objects.all().order_by('timestamp')[:50]
    return render(request, 'public_site/community_chat.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        
        if message_text:
            ChatMessage.objects.create(
                user=request.user,
                message=message_text
            )
        return redirect('community_chat')

@login_required
def financial_updates(request):
    financial_records = FinancialRecord.objects.all().order_by('-record_date')[:10]
    return render(request, 'public_site/financial.html', {'financial_records': financial_records})