from django.urls import path
from . import views

app_name = 'doctorapp'

urlpatterns = [
    path('doct/', views.Doctorfield, name='doctor'),
path('doctorname/', views.Forname, name='doct'),
    path('deta/', views.viewall, name='viewall'),
    path('patientdelete/<int:patient_id>/', views.DelView, name='delet'),
    path('patientmed/<int:patient_id>/', views.medical, name='med'),
    path('patienttreat/<int:patient_id>/', views.TreatView, name='treat'),
path('story/<int:patient_id>/', views.history, name='story'),
path('okay/', views.okay, name='okay'),


]

