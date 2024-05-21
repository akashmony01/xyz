from datetime import datetime, time
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    )

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    medical_history = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.date} at {self.time}"

    def clean(self):
        super().clean()

        # Check for existing appointments for the same patient at the same time
        if Appointment.objects.filter(patient=self.patient, date=self.date, time=self.time).exclude(
                pk=self.pk).exists():
            raise ValidationError(_("The patient already has an appointment at this time."))

        # Check for existing appointments for the same doctor at the same time
        if Appointment.objects.filter(doctor=self.doctor, date=self.date, time=self.time).exclude(pk=self.pk).exists():
            raise ValidationError(_("The doctor already has an appointment at this time."))

        # Check that the appointment is not in the past
        appointment_datetime = datetime.combine(self.date, self.time)
        if timezone.is_naive(appointment_datetime):
            appointment_datetime = timezone.make_aware(appointment_datetime, timezone.get_current_timezone())
        if appointment_datetime < timezone.now():
            raise ValidationError(_("The appointment cannot be in the past."))

    class Meta:
        unique_together = ('patient', 'doctor', 'date', 'time')


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medication} for {self.patient.name} by {self.doctor.name}"
