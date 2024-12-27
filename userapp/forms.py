from django import forms
from .models import Patient, Sex


class SexForm(forms.ModelForm):
    class Meta:
        model = Sex
        fields = ['sex']

        widgets = {
            'sex': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Select your sex',
            }),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'address', 'dateofbirth', 'email', 'sex','Image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address',
            }),
            'dateofbirth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Enter Date of Birth',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
            }),
            'sex': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select sex',
            }),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name', 'scheduled_time', 'Reason', 'age', 'dateofbirth',
            'address', 'phone_number', 'email', 'sex', 'Image'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name',
            }),
            'scheduled_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Enter scheduled time',
            }),
            'Reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the reason for appointment',
                'rows': 3,
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age',
            }),
            'dateofbirth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Enter Date of Birth',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address',
            }),
            'sex': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select sex',
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
            }),
        }

    def __init__(self, *args, **kwargs):
        # Extract token_number from kwargs
        token_number = kwargs.pop('token_number', None)
        super().__init__(*args, **kwargs)

        # Set initial value for token_number and make it readonly
        if token_number is not None:
            self.fields['token_number'].initial = token_number
            self.fields['token_number'].widget.attrs['readonly'] = True



