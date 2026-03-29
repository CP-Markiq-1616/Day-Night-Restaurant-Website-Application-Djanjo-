from django import forms
from Restaurant_02.models import Reservation_Model
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField



class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation_Model
        fields = "__all__"
        widgets = {
        "Requested_Date": forms.DateInput(attrs={"type":"date", "min":timezone.now().date()} ),
        "Requested_Time": forms.TimeInput( attrs={"type":"time"})
        }

class Checkout_ScreenForm(forms.Form):
    Customer_Name = forms.CharField (max_length=100, required=True, error_messages={"required":" "})
    Customer_Phone_Number = forms.CharField(max_length=20, required=True, error_messages={"required":" "}, widget=forms.TextInput(attrs={"placeholder": "ex 854-554-7745"}))
    Customer_Email= forms.EmailField(max_length=100, required=True, error_messages={"required":" "})
    Notes = forms.CharField (max_length=100, required=False)
    # customer_phone_number_form = PhoneNumberField()




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text= "Enter a valid email")
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("This email is already resigtered")
        return email