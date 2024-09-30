from django import forms
from .api_services import (
    get_genres,
)  # Import the function that fetches genres from TMDB
from .models import Review  # Import the Review model for handling reviews


# Form for filtering movies based on criteria such as rating, release date, popularity, and genre
class MovieFilterForm(forms.Form):
    # Field to filter movies based on minimum rating
    min_rating = forms.FloatField(
        label="Minimum Rating",  # Label for the field
        min_value=0,  # Minimum value allowed for the rating
        max_value=10,  # Maximum value allowed for the rating
        required=False,  # Field is optional
    )

    # Field to filter movies by release date starting from a specific year
    release_date_from = forms.IntegerField(
        label="Release Year From",  # Label for the field
        required=False,  # Field is optional
        widget=forms.NumberInput(
            attrs={"placeholder": "Year"}
        ),  # Add a placeholder in the input box
        min_value=1900,  # Minimum valid year for release
        max_value=2100,  # Maximum valid year for release
    )

    # Field to filter movies by release date up to a specific year
    release_date_to = forms.IntegerField(
        label="Release Year To",  # Label for the field
        required=False,  # Field is optional
        widget=forms.NumberInput(
            attrs={"placeholder": "Year"}
        ),  # Add a placeholder in the input box
        min_value=1900,  # Minimum valid year for release
        max_value=2100,  # Maximum valid year for release
    )

    # Field to filter movies by minimum popularity
    min_popularity = forms.FloatField(
        label="Minimum Popularity",  # Label for the field
        min_value=0,  # Minimum value allowed for popularity
        max_value=10,  # Maximum value allowed for popularity
        required=False,  # Field is optional
    )

    # Field to filter movies by genre, allowing multiple selections
    genres = forms.MultipleChoiceField(
        label="Genres",  # Label for the field
        choices=get_genres(),  # Get a list of genres fetched from the TMDB API via get_genres()
        required=False,  # Field is optional
        widget=forms.CheckboxSelectMultiple,  # Display genres as checkboxes for multiple selections
    )


# Form to submit a review for a movie
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Specify that this form is based on the Review model
        fields = [
            "content",
            "rating",
        ]  # Specify which fields from the model to include in the form

        # Define custom widgets (HTML elements) for the fields
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light",  # Custom CSS classes for styling the textarea
                    "placeholder": "Write your review here...",  # Placeholder text
                    "rows": 5,  # Set the number of rows (height) of the textarea
                }
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control bg-dark text-light",  # Custom CSS classes for styling the number input
                    "min": 1,  # Set minimum rating value
                    "max": 10,  # Set maximum rating value
                    "placeholder": "Rate the movie (1-10)",  # Placeholder text for the rating input
                }
            ),
        }
