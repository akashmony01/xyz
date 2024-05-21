from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:pk>/', views.delete_patient, name='delete_patient'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/add/', views.add_doctor, name='add_doctor'),
    path('doctor/edit/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('doctor/delete/<int:pk>/', views.delete_doctor, name='delete_doctor'),

    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointment/add/', views.add_appointment, name='add_appointment'),
    path('appointment/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointment/delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
]