from django import forms
from .models import Insurance,Bill,Report
from userapp.models import Patient
from doctorapp.models import DoctorPatient,Doctor

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['provider_name', 'logo', 'maximum_coverage', 'policy_number', 'coverage_percentage']

        widgets = {
            'provider_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Provider's Name",
            }),
            'maximum_coverage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Maximum Coverage Amount',
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
            'policy_number': forms.TextInput(attrs={  # Correct widget for textual policy numbers
                'class': 'form-control',
                'placeholder': 'Enter Policy Number',
            }),
            'coverage_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Coverage Percentage (e.g., 80)',
            }),
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            'injection_amount',
            'scanning_amount',
            'drugs_amount',
            'surgery_amount',
            'ward_procedures',
            'doctor_fee',
            'issue_date',
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'doctor_name',
            'scheduledtime',
            'reason',
            'treatment',
        ]
        widgets = {
            'scheduledtime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
