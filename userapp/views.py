from itertools import count
from urllib.request import Request

import stripe
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import JsonResponse

from .forms import PatientForm,SexForm,BookingForm
from .models import Patient,Sex
from django.shortcuts import get_object_or_404, redirect, render
from doctorapp.models import Doctor,DoctorPatient
from datetime import datetime
from adminapp.models import Insurance, Bill,Report

current_time = datetime.now()


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('userapp:home')
        else:
            messages.error(request, 'Please provide correct details.')
            return redirect('userapp:login')

    return render(request, 'user/login.html')

def userHomepage(request):
    return render(request, 'user/home.html')



def userindex(request):
    doctors = Doctor.objects.all()

    return render(request, 'user/index.html', {'doctors': doctors})


def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'This email is already taken.')
            else:
                User.objects.create_user(username=username, first_name=first_name,
                                         last_name=last_name, email=email, password=password)
                return redirect('userapp:login')
        else:
            messages.info(request, 'Passwords do not match.')

    return render(request, 'user/registration.html')
def Create_gender(request):
    if request.method == 'POST':

        form= SexForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect ('userapp:appointment')
    else:
        form=SexForm()

    return render (request,'user/gender.html',{'form':form})

def all(request):

    patients = Patient.objects.all().order_by('scheduled_time')

    for index, patient in enumerate(patients, start=1):
        patient.token_number = index

    return render(request, 'user/all.html', {'patients': patients})



def DeleteView(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        patient.is_deleted = True
        patient.delete()
        return redirect("userapp:all")

    return render(request, 'user/delete.html', {'patients': patient})


def updatepatient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("userapp:all")
    else:

        form = PatientForm(instance=patient)


    return render(request, 'user/update.html', {
        'form': form,
        'update': 'recently updated!',
    })

def details(request,patient_id):
    patients = Patient.objects.get(id=patient_id)


    return render(request, 'user/details.html', {'patients': patients})
def appointment(request):
    doctors = Doctor.objects.all()
    current_time = datetime.now()

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)

        if form.is_valid():
            patient = form.save(commit=False)

            patient.name = f"{request.user.first_name} {request.user.last_name}"
            patient.email = request.user.email

            patient.save()

            messages.success(request, 'Your appointment has been successfully registered.')
            return redirect('book')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        full_name = f"{request.user.first_name} {request.user.last_name}"
        email = request.user.email
        form = PatientForm(initial={'name': full_name, 'email': email})

    return render(request, 'user/register.html', {'form': form, 'doctors': doctors,'current_time':current_time})


def create_Booking(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to book an appointment.")
        return redirect('userapp:login')

    if Patient.objects.filter(user=request.user).exists():
        messages.warning(request, "You already have an appointment booked!")
        return render(request, 'user/already_registered.html')

    if request.method == 'POST':
        token_number = Patient.objects.count() + 1
        form = BookingForm(request.POST, request.FILES)

        if form.is_valid():
            patient_instance = form.save(commit=False)
            patient_instance.user = request.user
            patient_instance.token_number = token_number
            patient_instance.username = request.user.username
            patient_instance.name = f"{request.user.first_name} {request.user.last_name}"
            patient_instance.email = request.user.email
            patient_instance.username = request.user.username
            patient_instance.save()
            messages.success(request, "Your booking was successful!")
            return redirect('userapp:book')
        else:
            messages.error(request, "There were errors in the form. Please fix them.")
    else:
        form = BookingForm(initial={
            'username': request.user.username,
            'email': request.user.email,
        })
        token_number = Patient.objects.count() + 1

    return render(request, 'user/Booking.html', {'form': form, 'token_number': token_number})

def search_view(request):
    query = request.GET.get('q', '').strip()
    patients = []

    if query:
        try:
            token_query = int(query)
            patients = Patient.objects.filter(token_number=token_query).order_by('scheduled_time')
        except ValueError:
            patients = Patient.objects.filter(name__icontains=query).order_by('scheduled_time')

    if not query or not patients:
        patients = Patient.objects.filter(name__icontains=query) | Patient.objects.filter(token_number__icontains=query)

    for index, patient in enumerate(patients, start=1):
        patient.token_number = index

    return render(request, 'user/search_results.html', {'patients': patients, 'query': query})

def healthtips(request):
    return render(request, 'user/healthtips.html')

def user_insurance_details(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = None

    # Fetch the logged-in user's insurance details
    user_insurances = Insurance.objects.filter(user=request.user)

    doctor_patients = DoctorPatient.objects.filter(patient=patient) if patient else None

    context = {
        'patient': patient,
        'user_insurances': user_insurances,
        'doctor_patients': doctor_patients,
    }

    return render(request, 'user/insuranceprovide.html', context)


def Billview(request):
    # Fetch the logged-in user's patient profile
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = None


    user_bills = Bill.objects.filter(user=request.user)

    for bill in user_bills:
        bill.total_amount = (
            (bill.injection_amount or 0) +
            (bill.scanning_amount or 0) +
            (bill.drugs_amount or 0) +
            (bill.surgery_amount or 0) +
            (bill.ward_procedures or 0) +
            (bill.doctor_fee or 0)
        )


    doctor_patients = DoctorPatient.objects.filter(patient=patient) if patient else None

    context = {
        'patient': patient,
        'user_bills': user_bills,
        'doctor_patients': doctor_patients,
    }

    return render(request, 'user/bill.html', context)

def create_checkout_session(request, bill_id):
    """
    Create a Stripe Checkout session for a specific bill.
    """
    bill = get_object_or_404(Bill, id=bill_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        line_items = [
            {
                'price_data': {
                    'currency': 'inr',  # Stripe expects lowercase currency codes
                    'unit_amount': int(bill.total_amount * 100),  # Convert to the smallest currency unit
                    'product_data': {
                        'name': f"Medical Bill for {{ patient.name }}",
                    },
                },
                'quantity': 1,
            }
        ]

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('userapp:success')),  # URL for successful payment
                cancel_url=request.build_absolute_uri(reverse('userapp:cancel')),  # URL for canceled payment
            )

            return redirect(checkout_session.url, code=303)

        except stripe.error.StripeError as e:
            return JsonResponse({'error': f"Stripe error: {str(e)}"}, status=500)
        except Exception as e:

            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=405)
def payment_success(request):
    """
    A view to handle payment success. This view updates the bill status
    to 'Completed' and renders a success message.
    """
    bill_id = request.GET.get('bill_id')
    if not bill_id:
        return render(request, 'user/success.html', {
            'message': "Payment successful, but no bill ID was provided.",
        })

    # Fetch the bill object and update its status
    bill = get_object_or_404(Bill, id=bill_id)
    bill.status = 'Completed'
    bill.save()

    return render(request, 'user/success.html', {
        'message': "Your payment was successful! Thank you for your purchase.",
        'bill': bill,
    })
def payment_cancel(request):
    """
    A view to handle payment success. This view can be rendered after
    the user successfully completes a payment.
    """
    return render(request, 'user/cancel.html', {
        'message': "Your payment was successful! Thank you for your purchase.",
    })


def medicalhistory(request):

    patient = get_object_or_404(Patient, user=request.user)
    user_reports = Report.objects.filter(user=request.user)

    visits = DoctorPatient.objects.filter(patient=patient)

    if not visits:
        message = "No medical history available for this patient."
    else:
        message = None

    doctors = Doctor.objects.filter(id__in=visits.values('doctor_id'))

    # Pass patient, doctors, doctor-patient relationships, and message to the template
    return render(request, 'user/medicalhistory.html', {
        'patient': patient,
        'reports': user_reports,  # Update variable name to match the template
        'doctors': doctors,
        'visits': visits,
        'message': message,
        # Optional message for patients with no medical history
    })
