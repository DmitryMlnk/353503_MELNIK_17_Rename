from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date, timezone
import re
from .models import Review, CarType, Master

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(max_length=17, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'birth_date', 'phone_number')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return birth_date

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        pattern = r'^\+375\((?:25|29|33|44)\)\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone_number):
            raise forms.ValidationError("Phone number must be in the format +375(29)xxx-xx-xx.")
        return phone_number

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(label='Rating', min_value=0, max_value=10)

    class Meta:
        model = Review
        fields = ['rating', 'text']

class OrderForm(forms.Form):
    address = forms.CharField(max_length=255, required=True)
    scheduled_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    car_type = forms.ModelChoiceField(queryset=CarType.objects.all(), required=True)
    master = forms.ModelChoiceField(queryset=Master.objects.all(), required=True)

    def clean_scheduled_at(self):
        scheduled_at = self.cleaned_data.get('scheduled_at')
        if scheduled_at < timezone.now():
            raise forms.ValidationError("Scheduled time cannot be in the past.")
        return scheduled_at