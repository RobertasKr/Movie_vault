from django.shortcuts import render, redirect
from .forms import (
    ContactForm,
)  # Importing the contact form for users to submit messages
from .models import ContactFeedback  # Model for storing user feedback
from django.contrib.auth.decorators import (
    user_passes_test,
)  # Decorator to check if a user has specific permissions
from movies.api_services import (
    get_random_movies,
)  # Import function to fetch random movies from an external API

# API keys and base URL for The Movie Database (TMDB) API.
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MjRmNGRjYTE4NzUxOWMxM2VhOTExNWZhODFhZWJkMiIsIm5iZiI6MTcyNDA4NTYyMS41NzQyNTcsInN1YiI6IjY2YzM3M2VmYTVhMzA5ZTUyODVjZmMzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.h8y7gVwgKw6uVL_IyA3GCaFhk_jbDUKI_zPi5hBYINs"
API_KEY_SHORT = "524f4dca187519c13ea9115fa81aebd2"
BASE_URL = "https://api.themoviedb.org/3/"


# Function to check if a user is a superuser (admin).
# This is used by the @user_passes_test decorator to grant access to certain views only to superusers.
def is_superuser(user):
    return user.is_superuser  # Returns True if the user is a superuser, otherwise False


# View that only superusers can access, thanks to the @user_passes_test decorator.
# This view renders the admin page.
@user_passes_test(is_superuser)
def admin_view(request):
    return render(
        request, "admin_page.html"
    )  # Renders the 'admin_page.html' template for the superuser


# Home view that fetches random movies using the TMDB API.
# Displays six random movies on the homepage.
def home_view(request):
    try:
        # Attempt to fetch 6 random movies from the TMDB API.
        movies = get_random_movies(API_KEY)[:6]
    except Exception as e:
        # If the API request fails, display an empty movie list and print the error to the console.
        movies = []
        print(f"Failed to fetch movies: {e}")

    context = {"movies": movies}  # Pass the movies to the template context
    return render(request, "home.html", context)  # Render the 'home.html' template


# About page view that renders the about page.
def about_view(request):
    return render(request, "about.html")  # Render the 'about.html' template


# View to handle the contact form submission.
# Allows users to submit their name, email, and a message.
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)  # Create form instance with the POST data
        if form.is_valid():
            # If the form is valid, save the contact feedback to the database
            form.save()
            return redirect(
                "contacts_success"
            )  # Redirect to the success page after submission
    else:
        # If it's a GET request, display an empty contact form
        form = ContactForm()

    # Render the 'contacts.html' template with the form
    return render(request, "contacts.html", {"form": form})


# View to display all feedback submissions, accessible only to superusers.
@user_passes_test(is_superuser)
def feedback_view(request):
    # Retrieve all feedback entries from the ContactFeedback model, ordered by creation date (newest first)
    feedback_list = ContactFeedback.objects.all().order_by("-created_at")

    # Render the 'contacts_feedback.html' template, passing the feedback list as context
    return render(request, "contacts_feedback.html", {"feedback_list": feedback_list})


# View to display a success message after a successful contact form submission.
def contact_success_view(request):
    return render(
        request, "contacts_success.html"
    )  # Render the 'contacts_success.html' template
