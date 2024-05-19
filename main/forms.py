from django import forms
from .models import User, Assignment
from django.utils import timezone
import hashlib

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        hashed_password = hashlib.sha256(self.cleaned_data["password"].encode()).hexdigest()
        user.password = hashed_password
        user.user_type = 'student'
        user.is_superuser = False
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].widget.attrs['min'] = str(timezone.now().date())
        self.fields['students'].queryset = User.objects.filter(user_type='student')

    class Meta:
        model = Assignment
        fields = ['subject', 'due_date', 'description', 'students']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }