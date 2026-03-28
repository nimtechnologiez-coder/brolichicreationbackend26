from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Application
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

# API for React
def api_jobs(request):
    print("[DEBUG] /api/jobs/ endpoint hit!")
    jobs = Job.objects.all().order_by('-posted_at')
    jobs_list = []
    for job in jobs:
        jobs_list.append({
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'department': job.department,
            'type': job.job_type,       # For backwards compatibility
            'job_type': job.job_type,   # For common React component expectations
            'description': job.description,
            'responsibilities': [r.strip() for r in job.responsibilities.split('\n') if r.strip()] if job.responsibilities else [],
            'requirements': [r.strip() for r in job.requirements.split('\n') if r.strip()] if job.requirements else [],
            'posted_at': job.posted_at.strftime('%Y-%m-%d %H:%M:%S') if job.posted_at else None,
        })
    return JsonResponse(jobs_list, safe=False)

@csrf_exempt
def api_apply(request):
    if request.method == 'POST':
        try:
            # Handle both JSON and Multipart data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                job_id = data.get('job_id')
                name = data.get('name')
                email = data.get('email')
                cover_letter = data.get('cover_letter')
                resume = None
            else:
                job_id = request.POST.get('job_id')
                name = request.POST.get('name')
                email = request.POST.get('email')
                cover_letter = request.POST.get('cover_letter')
                resume = request.FILES.get('resume')

            job = get_object_or_404(Job, id=job_id)
            
            Application.objects.create(
                name=name,
                email=email,
                job=job,
                cover_letter=cover_letter,
                resume=resume
            )
            return JsonResponse({'status': 'success', 'message': 'Application submitted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

# Admin Login Page
def admin_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        print(f"[DEBUG] Login attempt for: {u}")
        
        # If an email is provided, map it to the corresponding username
        from django.contrib.auth.models import User
        if u and '@' in u:
            try:
                user_obj = User.objects.get(email=u)
                
                # Keep original u for logging, use username for auth
                auth_u = user_obj.username
            except User.DoesNotExist:
                auth_u = u
        else:
            auth_u = u
            
        user = authenticate(request, username=auth_u, password=p)
        if user is not None:
            print(f"[DEBUG] Auth SUCCESS for: {u}")
            login(request, user)
            return redirect('admin_dashboard')
        else:
            print(f"[DEBUG] Auth FAILED for: {u}. Checking database...")
            from django.contrib.auth.models import User
            db_user = User.objects.filter(username=u).first()
            if db_user:
                 print(f"[DEBUG] User {u} EXISTS in DB. Password mismatch?")
            else:
                 print(f"[DEBUG] User {u} DOES NOT EXIST in DB.")
            messages.error(request, "Invalid Credentials")
            return render(request, 'AdminLogin.html')
    return render(request, 'AdminLogin.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Dashboard Page
@login_required(login_url='admin_login')
@never_cache
def admin_dashboard(request):
    total_jobs = Job.objects.all().count()
    total_applications = Application.objects.all().count()
    recent_jobs = Job.objects.all().order_by('-posted_at')[:5]

    return render(request, 'AdminDashboard.html', {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'jobs': recent_jobs
    })


# Add Job Page
@login_required(login_url='admin_login')
@never_cache
def add_job(request):
    # ... logic ...
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        department = request.POST.get('department')
        if not department:
            department = 'Transports & Logistics'
        job_type = request.POST.get('job_type')
        description = request.POST.get('description')
        responsibilities = request.POST.get('responsibilities')
        requirements = request.POST.get('requirements')
        
        Job.objects.create(
            title=title, 
            location=location,
            department=department,
            job_type=job_type, 
            description=description,
            responsibilities=responsibilities,
            requirements=requirements
        )
        return redirect('job_list')
    return render(request, 'Addjob.html')


# Job List Page
@login_required(login_url='admin_login')
@never_cache
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'job_list.html', {'jobs': jobs})


# Applications Page
@login_required(login_url='admin_login')
@never_cache
def applications(request):
    filter_date = request.GET.get('date')
    apps = Application.objects.all().order_by('-applied_at')

    if filter_date:
        parsed_date = parse_date(filter_date)
        if parsed_date:
            apps = apps.filter(applied_at__date=parsed_date)

    return render(request, 'applications.html', {'applications': apps, 'filter_date': filter_date})


# Logic to update job
@login_required(login_url='admin_login')
@never_cache
def update_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, id=job_id)
        job.title = request.POST.get('title', job.title)
        job.location = request.POST.get('location', job.location)
        job.department = request.POST.get('department', job.department)
        job.job_type = request.POST.get('job_type', job.job_type)
        job.description = request.POST.get('description', job.description)
        job.responsibilities = request.POST.get('responsibilities', job.responsibilities)
        job.requirements = request.POST.get('requirements', job.requirements)
        job.save()
    return redirect('job_list')


# Logic to delete job
@login_required(login_url='admin_login')
@never_cache
def delete_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, id=job_id)
        job.delete()
    return redirect('job_list')


# Logic to delete application
@login_required(login_url='admin_login')
@never_cache
def delete_application(request, app_id):
    if request.method == 'POST':
        app = get_object_or_404(Application, id=app_id)
        app.delete()
    return redirect('applications')