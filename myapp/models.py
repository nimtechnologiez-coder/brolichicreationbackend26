from django.db import models

class Job(models.Model):
    JOB_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default='Transports & Logistics')
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    description = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True, help_text="Enter one responsibility per line")
    requirements = models.TextField(blank=True, null=True, help_text="Enter one requirement per line")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"
