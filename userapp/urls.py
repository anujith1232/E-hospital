from django.urls import path
from . import views

app_name = 'userapp'

urlpatterns = [
    path('', views.userRegister, name='reg'),
    path('login/', views.userlogin, name='login'),
path('home/', views.userHomepage, name='home'),
path('index/', views.userindex, name='index'),
path('app/',views.appointment,name='appointment'),
path('book/',views.create_Booking,name='book'),
path('gen/',views.Create_gender,name='gen'),
path('det/',views.all,name='all'),
    path('patient-delete/<int:patient_id>/', views.DeleteView, name='delete'),
    path('patient-update/<int:patient_id>/', views.updatepatient, name='update'),
    path('patient-details/<int:patient_id>/', views.details, name='details'),
    path('search/', views.search_view, name='search'),
path('tips/', views.healthtips, name='tips'),
path('provide/', views.user_insurance_details, name='insuranceprovide'),
path('patient-bills/', views.Billview, name='bills'),
path('checkout/<int:bill_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('history/',views.medicalhistory,name='history'),

]