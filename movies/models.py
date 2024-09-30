from django.db import models
from django.contrib.auth.models import (
    User,
)  # Importing the default User model from Django for user associations


# Model representing a movie genre
class Genre(models.Model):
    name = models.CharField(
        max_length=100
    )  # Name of the genre, with a maximum length of 100 characters

    def __str__(self):
        return (
            self.name
        )  # Return the genre's name when converting to string (useful for admin or display purposes)


# Model representing a movie
class Movie(models.Model):
    title = models.CharField(max_length=200)  # Title of the movie
    description = models.TextField()  # A detailed description of the movie
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE
    )  # Foreign key linking the movie to its genre
    release_date = models.DateField()  # Date when the movie was released
    rating = models.DecimalField(
        max_digits=3, decimal_places=1
    )  # Movie rating (up to 999 with 1 decimal place)
    tmdb_id = (
        models.IntegerField()
    )  # TMDB (The Movie Database) movie ID to link with the external API

    def __str__(self):
        return (
            self.title
        )  # Return the movie title when converting to string (useful for admin or display purposes)


# Model representing a user's watchlist
class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Foreign key linking the watchlist to the user
    movie_id = models.CharField(max_length=20)  # The TMDB movie ID for the movie
    movie_title = models.CharField(max_length=255)  # The title of the movie
    movie_poster = models.URLField(
        max_length=500, null=True, blank=True
    )  # URL for the movie poster image
    description = models.TextField(
        null=True, blank=True
    )  # Optional description of the movie
    genre = models.CharField(
        max_length=255, null=True, blank=True
    )  # Genre of the movie
    release_date = models.CharField(
        max_length=10, null=True, blank=True
    )  # Release date of the movie in string format
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )  # Optional rating of the movie
    watched = models.BooleanField(
        default=False
    )  # Boolean field to track if the movie has been watched

    def __str__(self):
        return (
            self.movie_title
        )  # Return the movie title when converting to string (useful for admin or display purposes)


# Model representing a review of a movie
class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Foreign key linking the review to the user who wrote it
    movie_id = (
        models.IntegerField()
    )  # The TMDB movie ID to identify which movie the review is about
    rating = models.IntegerField()  # Rating given by the user (typically between 1-10)
    content = models.TextField()  # The content or text of the user's review
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set the field to the current date and time when the review is created

    def __str__(self):
        return f"{self.user.username} - {self.movie_id}"  # Return the username and movie ID for display purposes
