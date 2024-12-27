from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('control/', views.control, name='control'),
path('', views.control, name=''),
path('', views.control, name='control'),
path('infos/',views.alldetails,name='alldetails'),
path('ins/', views.insuranceinfo, name='insert'),
path('insurance-details/<int:patient_id>/', views.insurance, name='insurance_details'),
path('insuranceview/<int:patient_id>/', views.insuranceview, name='insurance_v'),
path('bill/<int:patient_id>/', views.create_bill, name='bill'),
path('report/<int:patient_id>/', views.ReportView, name='reportentry'),
]
