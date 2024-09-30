from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User


# Custom form for handling user password changes
# This form extends Django's built-in PasswordChangeForm but customizes the field widgets
# to use Bootstrap's 'form-control' class for better styling in templates.
class CustomPasswordChangeForm(PasswordChangeForm):
    # The user's current password
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),  # Password input widget with Bootstrap styling
        label="Current Password",  # Label for the field in the form
    )

    # The new password the user wants to set
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),  # Password input widget with Bootstrap styling
        label="New Password",  # Label for the field in the form
    )

    # Confirmation field for the new password (must match new_password1)
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),  # Password input widget with Bootstrap styling
        label="Confirm New Password",  # Label for the field in the form
    )


# Custom form for user registration that extends Django's UserCreationForm
# This form allows the user to sign up with an email and password.
# It also validates that the email is unique within the system.
class CustomUserCreationForm(UserCreationForm):
    # Email field is required and must be valid
    email = forms.EmailField(
        required=True, help_text="Required. Inform a valid email address."
    )

    # Meta class defines the model and fields to include in the form
    class Meta:
        model = User  # The model this form is based on (Django's built-in User model)
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )  # Fields to display in the form

    # Custom validation to check if the email is already in use by another user
    def clean_email(self):
        email = self.cleaned_data.get("email")  # Get the email entered by the user
        if User.objects.filter(email=email).exists():
            # If a user with the entered email already exists, raise a validation error
            raise forms.ValidationError("Email is already in use.")
        return email  # If no user with the email exists, return the email
