from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Appointment
from .forms import PatientForm, DoctorForm, AppointmentForm

# Create your views here.
@login_required
def dashboard(request):

    context = {
        'patients' : Patient.objects.order_by('-created_at')[:5],
        'doctors': Doctor.objects.order_by('-created_at')[:5],
        'appointments': Appointment.objects.order_by('created_at')[:5],
    }
    return render(request, 'pages/index.html', context=context)


# ====================================================================================


def patient_list(request):
    patients = Patient.objects.order_by('-created_at')
    return render(request, 'pages/patient_list.html', {'patients': patients})


def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'pages/patient_form.html', {'form': form})


def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'pages/patient_form.html', {'form': form})


def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')


# ==========================================================================================

@login_required
def doctor_list(request):
    if not request.user.is_superuser:
        return redirect('permission_denied_page')
    doctors = Doctor.objects.all()

    return render(request, 'pages/doctor_list.html', {'doctors': doctors})


def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')  # Redirect to the doctor list page
    else:
        form = DoctorForm()
    return render(request, 'pages/doctor_form.html', {'form': form})

def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')  # Redirect to the doctor list page
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'pages/doctor_form.html', {'form': form, 'doctor': doctor})


def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')



# =================================================================================================
def appointment_list(request):
    if request.user.is_superuser:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(doctor__user=request.user)
    return render(request, 'pages/appointment_list.html', {'appointments': appointments})



def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'pages/appointment_form.html', {'form': form})


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'pages/appointment_form.html', {'form': form, 'appointment': appointment})


def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
