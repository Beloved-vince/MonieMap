from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, PasswordInput
from django.core.validators import RegexValidator, EmailValidator

class RegisterForm(Form):
    #Form Validation for neccessary authentication details
    
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email_validator = EmailValidator(message="Enter a valid email address.")
    email = EmailField(validators=[email_validator])
    phone_regex = RegexValidator(regex=r'^\d{1,11}$', message="Phone number must contain only digits (up to 11).")
    phone_number = CharField(validators=[phone_regex], max_length=11)
    password = CharField(widget=PasswordInput)
    password_confirm =  CharField(widget=PasswordInput)
    
    def clean_password_confirm(self):
        # password cleaning to avoid external attack(sql injection)
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise ValidationError("Password fields do not match")