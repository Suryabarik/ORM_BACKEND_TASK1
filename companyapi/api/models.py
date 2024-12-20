

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid

# Custom User Model with Role-Based Access Control (RBAC)
class User(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
        ('read_only', 'Read-Only'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='read_only')

    def __str__(self):
        return f"{self.username} ({self.role})"

# Patient Profile Management Model
class Patient(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_info = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True, null=True)
    known_allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="patients",
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.unique_id})"

# Digital Prescription Management Model
class Prescription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]

    patient = models.ForeignKey(
        Patient,
        related_name='prescriptions',
        on_delete=models.CASCADE,  # Delete prescriptions if the patient is deleted
        null=False,
        blank=False
    )
    medication_details = models.TextField()
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="prescriptions",
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    renewed_from = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='renewals'
    )

    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.last_name} ({self.id})"
    

