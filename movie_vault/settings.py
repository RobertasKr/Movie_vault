"""
Django settings for the movie_vault project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see:
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import (
    Path,
)  # Importing the Path class from pathlib for working with file paths
import os  # Importing os for environment variable handling

# BASE_DIR refers to the root directory of the project. It helps in building absolute paths within the project.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*wt$pcp&no0^ud3i0q$y-g4v6ltm%fgdy-x+iqe9-^$x$8(sdf"
# The SECRET_KEY is critical for the security of the Django project. In production, it should be kept private.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# In development, DEBUG is set to True for easier debugging, but should be False in production for security reasons.

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",  # Django's built-in admin interface
    "django.contrib.auth",  # Django's authentication system
    "django.contrib.contenttypes",  # Content types framework
    "django.contrib.sessions",  # Session management
    "django.contrib.messages",  # Messaging framework
    "django.contrib.staticfiles",  # Static file management (CSS, JavaScript, etc.)
    # Third-party apps
    "django_bootstrap5",  # Integration of Bootstrap 5 with Django templates
    # Local apps
    "movies",  # The movies app, handles movie-related functionality
    "accounts",  # The accounts app, handles user authentication and profiles
    "movie_vault",  # Main app of the project, contains project-level settings
]

# Middleware is a framework for processing requests/responses globally.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Provides security enhancements
    "django.contrib.sessions.middleware.SessionMiddleware",  # Manages sessions for logged-in users
    "django.middleware.common.CommonMiddleware",  # Provides common functionality such as URL rewriting
    "django.middleware.csrf.CsrfViewMiddleware",  # Prevents Cross-Site Request Forgery attacks
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Associates users with requests using sessions
    "django.contrib.messages.middleware.MessageMiddleware",  # Handles temporary messages
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Prevents clickjacking by adding headers
]

# URL configuration root for the project
ROOT_URLCONF = "movie_vault.urls"

# Template settings for rendering HTML files. Specifies where Django should look for template files.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Using Django's default template engine
        "DIRS": [
            BASE_DIR / "templates"
        ],  # Tells Django to look for templates in the 'templates' directory at the project root
        "APP_DIRS": True,  # Looks for templates in app directories as well
        "OPTIONS": {
            "context_processors": [  # Adds context to all templates automatically
                "django.template.context_processors.debug",  # Adds debug context if DEBUG=True
                "django.template.context_processors.request",  # Adds request object to all templates
                "django.contrib.auth.context_processors.auth",  # Adds user object to all templates
                "django.contrib.messages.context_processors.messages",  # Adds message framework data to templates
            ],
        },
    },
]

# WSGI configuration for the project, used by the server to run the Django application.
WSGI_APPLICATION = "movie_vault.wsgi.application"

# Database configuration. Uses SQLite as the default database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Default database engine (SQLite)
        "NAME": BASE_DIR / "db.sqlite3",  # Path to the SQLite database file
    }
}

# Password validation settings. Django provides several validators for enforcing password strength and security.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # Prevents use of personal info as passwords
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # Enforces a minimum length on passwords
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # Prevents use of common weak passwords
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # Prevents use of purely numeric passwords
    },
]

# Internationalization settings
LANGUAGE_CODE = "en-us"  # Default language for the project
TIME_ZONE = "UTC"  # Default timezone

USE_I18N = True  # Enables translation support
USE_TZ = True  # Enables timezone-aware datetimes

# Static files (CSS, JavaScript, Images) URL and configuration
STATIC_URL = "/static/"  # Base URL for serving static files

# Directory where static files will be collected for deployment
STATIC_ROOT = BASE_DIR / "staticfiles"

# Additional directories to find static files (e.g., for Bootstrap)
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type for models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The API key for TMDB (The Movie Database) is retrieved from environment variables for security
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# URL to redirect to after a successful login
LOGIN_REDIRECT_URL = "/home/"

# URL to redirect to after logout
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Email configuration for sending emails (e.g., for password resets)
EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"  # Backend for sending emails via SMTP
)
EMAIL_HOST = "smtp.gmail.com"  # Email server host (Gmail in this case)
EMAIL_PORT = 587  # Port for sending emails via TLS
EMAIL_USE_TLS = True  # Enables TLS encryption for secure email communication
EMAIL_HOST_USER = (
    "robertas.krasausk@gmail.com"  # Your Gmail address (for sending emails)
)
EMAIL_HOST_PASSWORD = "Ex68576jq3"  # Password for the Gmail account
DEFAULT_FROM_EMAIL = (
    EMAIL_HOST_USER  # Default email address used for sending system emails
)
