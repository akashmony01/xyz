# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Patient, Doctor, Appointment, Prescription

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'medical_history']


class DoctorForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['password'].widget.attrs['readonly'] = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not self.instance.pk and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def save(self, commit=True):
        if not self.instance.pk:  # Check if instance is being created
            user = User.objects.create_user(username=self.cleaned_data['username'],
                                            password=self.cleaned_data['password'])
            self.instance.user = user
        doctor = super().save(commit=False)
        if commit:
            doctor.save()
        return doctor



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'medication', 'dosage']
