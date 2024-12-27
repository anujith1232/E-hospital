from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from doctorapp.models import DoctorPatient, Doctor
from userapp.models import Patient
from .models import Insurance,Bill,Report
from .forms import InsuranceForm, BillForm,ReportForm


def control(request):
    patients = Patient.objects.all().order_by('scheduled_time')
    insurances = Insurance.objects.all()
    return render(request, 'admin/control.html', {'patients': patients, 'insurances': insurances})

@login_required
def alldetails(request):
    visits = DoctorPatient.objects.all()
    patients = Patient.objects.all().order_by('scheduled_time')

    # Assign token numbers for display purposes
    for index, patient in enumerate(patients, start=1):
        patient.token_number = index

    # Pass the data to the template
    context = {
        'patients': patients,
        'visits': visits,
    }
    return render(request, 'admin/allview.html', context)

@login_required
def insurance(request, patient_id):
    # Fetch the patient using the ID
    patient = get_object_or_404(Patient, id=patient_id)

    # Find insurance linked to the patient's user
    user_insurance = Insurance.objects.filter(user=patient.user).first()

    # Handle form submission
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES)
        if form.is_valid():
            if user_insurance:
                # If insurance already exists for the user, update it
                insurance = user_insurance
                form = InsuranceForm(request.POST, request.FILES, instance=insurance)
                insurance = form.save(commit=False)
                insurance.user = patient.user  # Make sure the insurance is linked to the patient’s user
                insurance.save()
            else:
                # If no insurance exists, create a new one
                insurance = form.save(commit=False)
                insurance.user = patient.user  # Link the insurance to the patient’s user
                insurance.save()

            return redirect('adminapp:alldetails')  # Redirect after successful form submission

    else:
        form = InsuranceForm(instance=user_insurance)  # Pre-fill form if there's an existing insurance record

    return render(request, 'admin/insurance.html', {
        'form': form,
        'patient': patient,
        'user_insurance': user_insurance
    })
@login_required
def insuranceinfo(request):
    insurances = Insurance.objects.all()
    patients_with_insurance = Patient.objects.filter(user__insurance__isnull=False)
    return render(request, 'admin/insuranceinfo.html', {'insurances': insurances, 'patients': patients_with_insurance})


@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        patient.delete()
        return redirect(reverse("adminapp:alldetails"))
    return render(request, 'admin/doctdelet.html', {'patient': patient})

@login_required
def insuranceview(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    insurance_record = Insurance.objects.filter(user=patient.user).first()

    return render(request, 'admin/insuranceview.html', {
        'patient': patient,
        'insurance': [insurance_record] if insurance_record else [],
    })

@login_required
def create_bill(request, patient_id):
    # Get the patient object
    patient = get_object_or_404(Patient, id=patient_id)
    success_message = None

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            # Save the bill and associate the logged-in user and patient with it
            bill = form.save(commit=False)  # Don't save yet
            bill.user = request.user  # Set the logged-in user
            bill.patient = patient  # Associate the bill with the selected patient
            bill.save()  # Now save the bill
            success_message = "Bill created successfully!"
            form = BillForm()  # Reset the form for a new entry
    else:
        form = BillForm()

    return render(request, 'admin/createbill.html', {
        'form': form,
        'success_message': success_message,
        'patient': patient,
    })
def ReportView(request, patient_id):
    # Fetch the patient using the ID
    patient = get_object_or_404(Patient, id=patient_id)

    # Find insurance linked to the patient's user
    user_report = Report.objects.filter(user=patient.user).first()

    # Handle form submission
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            if user_report:
                # If insurance already exists for the user, update it
                report = user_report
                form = ReportForm(request.POST, request.FILES, instance=insurance)
                report = form.save(commit=False)
                report.user = patient.user  # Make sure the insurance is linked to the patient’s user
                report.save()
            else:
                # If no insurance exists, create a new one
                report = form.save(commit=False)
                report.user = patient.user  # Link the insurance to the patient’s user
                report.save()

            return redirect('adminapp:book')  # Redirect after successful form submission

    else:
        form = ReportForm(instance=user_report)  # Pre-fill form if there's an existing insurance record

    return render(request, 'admin/report.html', {
        'form': form,
        'patient': patient,
        'user_report': user_report
    })

