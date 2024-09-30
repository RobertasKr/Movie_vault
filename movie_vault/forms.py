from django import forms
from .models import ContactFeedback


# This form is used to collect contact information and feedback from users.
# It is based on the ContactFeedback model and includes fields for name, email, and message.
class ContactForm(forms.ModelForm):
    # Meta class defines the model and the fields to be used in the form.
    class Meta:
        model = ContactFeedback  # This form is tied to the ContactFeedback model.

        # Specifies the fields that will be included in the form.
        fields = [
            "name",
            "email",
            "message",
        ]  # The form will have fields for the user's name, email, and message.

        # Customizes the widget for the 'message' field.
        widgets = {
            "message": forms.Textarea(
                attrs={"rows": 5}
            ),  # The 'message' field will use a Textarea widget with 5 rows.
        }
