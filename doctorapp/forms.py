from django import forms
from .models import Doctor, Name, DoctorPatient
from userapp.models import Patient  # Ensure correct import for Patient model

class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ['Doctorname']

        widgets = {
            'Doctorname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Doctor Name',
            }),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctor_name', 'schedule','Image','specialization']  # Adjusted the field name to match model

        widgets = {
            'doctor_name': forms.Select(attrs={  # Changed to Select for ForeignKey
                'class': 'form-control',
                'placeholder': 'Select Doctor Name',
            }),
            'schedule': forms.Textarea(attrs={  # Textarea might be more appropriate for schedules
                'class': 'form-control',
                'placeholder': 'Enter Doctor Schedule',
            }),
            'Image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
            'specialization': forms.TextInput(attrs={  # Changed to Select for ForeignKey
                'class': 'form-control',
                'placeholder': 'Select Doctor Name',
            }),
        }


class DoctorPatientForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.order_by('doctor_name'),
        empty_label="Select Doctor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = DoctorPatient
        fields = ['doctor', 'prescription', 'diagnosis']  # Ensure 'doctor' is a selectable field

        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Doctor Name',
            }),
            'prescription': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Prescription',
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Diagnosis',
            }),
        }
