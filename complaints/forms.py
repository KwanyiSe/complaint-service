from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'name', 'matricule', 'level', 'semester',   # ← new fields
            'school', 'phone_number',
            'complaint_number', 'submission_office', 'complaint_text',
            'course', 'course_code', 'ca_mark', 'exam_mark',
            'proof'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'matricule': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your matricule number'
            }),
            'level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 200, 300, 400, Masters'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., First Semester'
            }),
            'school': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Faculty of Science'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 670000000'
            }),
            'complaint_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint reference number'
            }),
            'submission_office': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "e.g., Dean's Office, Exams & Records"
            }),
            'complaint_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe what happened, what needs to be corrected, etc.'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Introduction to Computer Science'
            }),
            'course_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CSC101'
            }),
            'ca_mark': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 25/30'
            }),
            'exam_mark': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 60/70'
            }),
            'proof': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['payment_screenshot']
        widgets = {
            'payment_screenshot': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }