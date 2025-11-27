from django.shortcuts import render, redirect, get_object_or_404
from . import models as mod
from django.contrib import messages
from u_task.task import send_email
from student.models import Student_info
from teacher.models import Teacher
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q



def home(request):
    user_session = "guest"
    valid = "ADMIN"

    if request.user.is_authenticated:
        # Try to fetch Student_info first, then Teacher
        # Use select_related if user profile has foreign keys to user (assuming OneToOne or similar)
        try:
            user_session = Student_info.objects.get(user=request.user)
            valid = user_session.joined
        except Student_info.DoesNotExist:
            try:
                user_session = Teacher.objects.get(user=request.user)
            except Teacher.DoesNotExist:
                pass
    
    # Optimize queries
    # Use select_related/prefetch_related if models have relationships, 
    # but here we are mostly fetching flat lists or simple filters.
    
    # Fetch all data in parallel or optimized batches if possible, but Django is synchronous.
    # We can at least ensure we are not over-fetching.
    
    faculty = mod.Faculty_Teacher_Info.objects.all()
    name = mod.Header.objects.first()
    slider = mod.Slider.objects.all()
    
    # Combine News and Events if they are the same model, or keep separate if distinct logic needed.
    # Here they are same model 'News'.
    news_events = mod.News.objects.filter(
        Q(category='Notice') | Q(category='Events')
    ).order_by('-created_at')
    
    # Split them in python to save 1 DB query if list is small, 
    # but separate queries are fine for limit/offset.
    # Given limits are small (6 and 1), separate queries are okay.
    news = news_events.filter(category='Notice')[:6]
    event = news_events.filter(category='Events')[:1]

    photo = mod.GalleryImage.objects.all().order_by('-created_at')[:4]
    upcoming_events = mod.Event.objects.all().order_by('-created_at')[:1]
    achivement = mod.Achievements_stats.objects.first()
    students_review = mod.Student_Reviews.objects.all().order_by('-created_at')[:4] 
    
    context = {
        'title': name,
        'slides': slider,
        'news': news,
        'gallery_images': photo,
        'upcoming_events': upcoming_events,
        'achivement': achivement,
        'events': event,
        'user_session': user_session,
        'facultys': faculty,
        'joined': valid,
        'students_review': students_review,
    } 
    return render(request, "home/index.html", context)

def academics(request):
    achivement = mod.Achievements_stats.objects.first()
    grade = mod.Academics.objects.first()
    resource = mod.Academic_resources.objects.first()
    members = mod.Members.objects.all()
    
    # Handle Search
    query = request.GET.get('q')
    if query:
        members = mod.Members.objects.filter(
            Q(member_name__icontains=query) | 
            Q(member_contact__icontains=query)
        )
    
    paginator = Paginator(members, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { 
        'achivement': achivement,
        'grade': grade,
        'resource': resource,
        'members': page_obj,
        'query': query,
    }

    return render(request, "academics/academics.html", context)

def admission(request):
    resources = mod.Academic_resources.objects.first()
    context = {
        'resources': resources,
    }
    return render(request, "admision/admision.html", context)

def news(request):
    news_list = mod.News.objects.all()
    
    # Handle Search
    query = request.GET.get('q')
    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Handle Category Filter
    category = request.GET.get('category')
    if category and category != 'all':
        news_list = news_list.filter(category=category)
        
    # Handle Pagination
    paginator = Paginator(news_list, 12) # Show 6x2  news items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = { 
        'new_s': page_obj, 
        'query': query,
        'current_category': category,
    }
    return render(request, "News/news.html", context)

def gallery(request):
    images = mod.GalleryImage.objects.all()
    
    # Handle Search
    query = request.GET.get('q')
    if query:
        images = images.filter(
            Q(title__icontains=query) | 
            Q(category__icontains=query)
        )
    
    # Handle Category Filter
    category = request.GET.get('category')
    if category and category != 'all':
        images = images.filter(category=category)
        
    # Handle Pagination
    paginator = Paginator(images, 12) # Show 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = { 
        'images': page_obj,
        'query': query,
        'current_category': category,
    }

    return render(request, 'gallery/gallery.html', context)

def detail_news(request, pk):
    news = get_object_or_404(mod.News, id=pk)
    context = {
        'news': news,
    }
    return render(request, 'News/detail_news.html', context)

def achivement(request):
    return render(request, 'achivements/achivements.html')

def contact(request):
    if request.method == "POST":
        full_name = request.POST.get("name") 
        email = request.POST.get("email")
        contact = request.POST.get("phone")
        faculty = request.POST.get("subject")
        message = request.POST.get("message")
        subject = "to get admitted "
        
        # Get Head teachers emails
        # Optimize: Use values_list to fetch only emails directly
        list_teacher = list(User.objects.filter(groups__name='Head').values_list('email', flat=True))
        
        # Save contact to DB
        data = mod.Contact(full_name=full_name, email=email, contact=contact, faculty=faculty, message=message)
        data.save()
        
        full_message = f"""From: {full_name} <{email}>
        Subject: {subject}

        Dear Teacher,

                    You have received a new contact query from a student.

                    Full Name: {full_name}
                    Contact: {contact}
                    Email: {email}
                    Faculty: {faculty}

                    Message:
                            {message}

                    Best regards,
                    {full_name}
                    """

        # Send email asynchronously
        send_email.delay(
            subject=f"Contact Form: {subject}",
            message=full_message,
            sender=email,
            recivers=list_teacher
        )

        messages.success(request, "Sent Successfully!")
        return redirect('home:home')

    return render(request, "contact/contact.html")
