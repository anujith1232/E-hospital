from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import DoctorPatientForm, DoctorForm,NameForm
from .models import DoctorPatient, Doctor,Name
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from userapp.models import Patient
from adminapp.models import Report


# Create your views here.
def Forname(request):
    if request.method == 'POST':

        form= NameForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect ('doctorapp:doctor')
    else:
        form=NameForm()

    return render (request,'doctor/doctor.html',{'form':form})

def Doctorfield(request):
    if request.method == 'POST':

        form= DoctorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form=DoctorForm()

    return render (request,'doctor/doctfield.html',{'form':form})
def viewall(request):
    patients = Patient.objects.all().order_by('scheduled_time')


    for index, patient in enumerate(patients, start=1):
        patient.token_number = index

    return render(request, 'doctor/viewall.html', {'patients': patients})

def DelView(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        patient.delete()
        return redirect("doctorapp:doct")

    return render(request, 'doctor/delet.html', {'patients': patient})

def medical(request,patient_id):
    patients = Patient.objects.get(id=patient_id)


    return render(request, 'doctor/viewdetails.html', {'patients': patients})
def TreatView(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = DoctorPatientForm(request.POST)
        if form.is_valid():
            doctor_patient = form.save(commit=False)
            doctor_patient.patient = patient
            doctor_patient.save()
            return redirect('doctorapp:okay')
    else:
        form = DoctorPatientForm()

    return render(request, 'doctor/treat.html', {'form': form, 'patient': patient})
def okay(request):
    return render(request, 'doctor/okay.html')
def history(request,patient_id):
    patients = Patient.objects.get(id=patient_id)
    user_reports = Report.objects.all()

    visits = DoctorPatient.objects.all()

    doctors = Doctor.objects.all()

    return render(request, 'doctor/history.html', {
        'patients': patients,
        'reports': user_reports,
        'doctors': doctors,
        'visits': visits,
    })
