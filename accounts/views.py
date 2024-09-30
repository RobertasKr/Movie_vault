from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout as auth_logout
from .forms import CustomPasswordChangeForm, CustomUserCreationForm
from django.contrib import messages
from movies.models import Watchlist


# Custom view for user login
# Authenticates the user using Django's built-in `authenticate` function and logs them in if credentials are valid.
def custom_login_view(request):
    if request.method == "POST":
        # Extracting the username and password from the POST request
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user using Django's authentication system
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user exists and the credentials are correct, log them in
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("home")  # Redirect to the homepage after login
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid credentials")
    return render(
        request, "accounts/login.html"
    )  # Render the login page for GET request or failed login


# View to handle user registration
# This view displays a registration form and processes the form submission to create a new user.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Pass POST data to form
        if form.is_valid():
            # Save the form, which creates a new user in the database
            form.save()
            return redirect(
                "login"
            )  # Redirect to login page after successful registration
    else:
        # If it's a GET request, display an empty form
        form = CustomUserCreationForm()

    # Render the registration form
    return render(request, "accounts/register.html", {"form": form})


# View to handle user settings, specifically password changes
# This view allows logged-in users to change their password.
@login_required  # Ensures only authenticated users can access this view
def user_settings(request):
    if request.method == "POST":
        # Instantiate the password change form with POST data and the current user
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            # Save the new password for the user
            user = form.save()
            # Update the session so the user stays logged in after password change
            update_session_auth_hash(request, user)
            return redirect(
                "user_settings"
            )  # Redirect to the same page after successful password change
    else:
        # For a GET request, display the form with the current user context
        form = CustomPasswordChangeForm(user=request.user)

    # Render the user settings (password change) form
    return render(request, "accounts/user_settings.html", {"form": form})


# View to handle user logout
# This logs out the current user and redirects them to the login page.
@login_required
def user_logout(request):
    auth_logout(request)  # Log the user out using Django's built-in `logout` function
    return redirect("login")  # Redirect to the login page after logout


# View to display the user's watchlist
# This view retrieves all movies added to the logged-in user's watchlist and displays them.
@login_required
def view_watchlist(request):
    # Retrieve all watchlist movies that belong to the currently logged-in user
    watchlist_movies = Watchlist.objects.filter(user=request.user)

    # Render the watchlist page, passing the watchlist_movies as context
    return render(
        request, "accounts/watchlist.html", {"watchlist_movies": watchlist_movies}
    )
