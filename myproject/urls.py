from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from myapp import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-job/', views.add_job, name='add_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('applications/', views.applications, name='applications'),
    path('api/jobs/', views.api_jobs, name='api_jobs'),
    path('api/apply/', views.api_apply, name='api_apply'),
    # CRUD operations
    path('update-job/<int:job_id>/', views.update_job, name='update_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('delete-application/<int:app_id>/', views.delete_application, name='delete_application'),
    path('logout/', views.admin_logout, name='admin_logout'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]