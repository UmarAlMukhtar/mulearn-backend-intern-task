from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    # Job Types
    TYPE_CHOICES = (
        ('internship', 'Internship'),
        ('full-time', 'Full-time'),
        ('gig', 'Gig'),
    )
    # Location Types
    LOCATION_CHOICES = (
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    )
    # Job Status
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('verified', 'Verified'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Relationships
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='jobs'
    )
    skills = models.ManyToManyField(Skill, related_name='jobs')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.username}"