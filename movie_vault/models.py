from django.db import models


# Model to store feedback or messages submitted by users through a contact form
class ContactFeedback(models.Model):
    # Field to store the name of the user
    name = models.CharField(
        max_length=255
    )  # CharField is used for short text fields. max_length=255 limits the length of the name

    # Field to store the email address of the user
    email = (
        models.EmailField()
    )  # EmailField automatically validates that the input is a valid email address

    # Field to store the message provided by the user
    message = (
        models.TextField()
    )  # TextField is used for larger text input like messages or feedback

    # Field to store the date and time when the feedback was created
    # auto_now_add=True ensures that the current date and time are automatically saved when a new record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # A string representation method for displaying feedback in a readable format (e.g., in the admin panel)
    def __str__(self):
        return f"Message from {self.name} ({self.email})"  # Returns the name and email of the user in a string format
