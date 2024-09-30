from .models import (
    Movie,
    Review,
    Watchlist,
)  # Import models for movies, reviews, and watchlists
from .api_services import (
    get_trending_movies,
    get_random_movies,
    get_movie_details,
    fetch_movies_from_tmdb,
)  # Import API services
from .forms import (
    MovieFilterForm,
    ReviewForm,
)  # Import forms for filtering movies and writing reviews
from django.core.paginator import Paginator  # Paginator for pagination
from django.contrib import (
    messages,
)  # Used to display success, warning, or error messages
from django.contrib.auth.decorators import (
    login_required,
)  # Decorator to ensure views are only accessed by logged-in users
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)  # Helpers for rendering, redirecting, and object retrieval
import requests  # Requests library for making external API calls

# API keys for TMDB (The Movie Database) to make requests for movie data
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MjRmNGRjYTE4NzUxOWMxM2VhOTExNWZhODFhZWJkMiIsIm5iZiI6MTcyNDA4NTYyMS41NzQyNTcsInN1YiI6IjY2YzM3M2VmYTVhMzA5ZTUyODVjZmMzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.h8y7gVwgKw6uVL_IyA3GCaFhk_jbDUKI_zPi5hBYINs"
API_KEY_SHORT = "524f4dca187519c13ea9115fa81aebd2"


# View for handling movie searches
def movie_search(request):
    query = request.GET.get("query", "")  # Get the search query from the GET request
    movies = []  # Initialize an empty list to store movies

    if query:
        # Make a request to TMDB API to search for movies by title
        tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY_SHORT}&query={query}"
        response = requests.get(tmdb_url)

        if response.status_code == 200:
            data = response.json()
            movies = data.get(
                "results", []
            )  # Extract the list of movies from the API response

    context = {
        "movies": movies,
        "query": query,  # Pass the query and movies to the template
    }
    return render(request, "movies/search_results.html", context)


# View for displaying a list of all movies in the database
def movie_list(request):
    movies = Movie.objects.all()  # Retrieve all movies from the Movie model
    return render(request, "movies/movie_list.html", {"movies": movies})


# View to display the details of a specific movie (by its TMDB ID)
@login_required
def movie_detail(request, tmdb_id):
    # Fetch movie data from TMDB API using the movie's TMDB ID
    movie_data = get_movie_details(API_KEY, tmdb_id)

    # Retrieve reviews for the movie from the database
    reviews = Review.objects.filter(movie_id=tmdb_id)

    # Check if the logged-in user has already reviewed this movie
    existing_review = Review.objects.filter(movie_id=tmdb_id, user=request.user).first()

    if request.method == "POST":
        # If a POST request is received, save the review (if it already exists, update it)
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = tmdb_id
            review.user = request.user
            review.save()
            return redirect("movie_detail", tmdb_id=tmdb_id)
    else:
        # Pre-fill the form with the user's existing review (if any)
        form = ReviewForm(instance=existing_review)

    # Render the movie details along with the review form and reviews
    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie": movie_data,
            "form": form,
            "reviews": reviews,
        },
    )


# View to delete a review written by the user
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(
        Review, id=review_id
    )  # Get the review or return a 404 if not found

    # Check if the logged-in user is the author of the review
    if review.user == request.user:
        review.delete()  # Delete the review
        return redirect("movie_detail", tmdb_id=review.movie_id)
    else:
        # If the user is not the author, redirect to the movie details without deleting
        return redirect("movie_detail", tmdb_id=review.movie_id)


# View to display trending movies (fetched from TMDB API)
def trending_movies(request):
    movies = get_trending_movies(API_KEY)  # Fetch trending movies from TMDB
    return render(request, "movies/trending_movies.html", {"movies": movies})


# View to display random movies (fetched from TMDB API)
def show_movies(request):
    movies = get_random_movies(API_KEY)  # Get random movies from TMDB
    return render(request, "movies/movies_random.html", {"movies": movies})


# View to filter movies based on user criteria
def filter_movies(request):
    form = MovieFilterForm(request.GET or None)  # Initialize the filter form
    movies = []  # Empty list to hold filtered movies

    if form.is_valid():
        # Extract the filter criteria from the form
        min_rating = form.cleaned_data.get("min_rating")
        release_date_from = form.cleaned_data.get("release_date_from")
        release_date_to = form.cleaned_data.get("release_date_to")
        min_popularity = form.cleaned_data.get("min_popularity")
        selected_genres = form.cleaned_data.get("genres")

        # Construct the TMDB API URL with the filter criteria
        tmdb_url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY_SHORT}&sort_by=popularity.desc"

        # Append filters to the API URL
        if min_rating:
            tmdb_url += f"&vote_average.gte={min_rating}"
        if release_date_from:
            tmdb_url += f"&primary_release_date.gte={release_date_from}-01-01"
        if release_date_to:
            tmdb_url += f"&primary_release_date.lte={release_date_to}-12-31"
        if min_popularity:
            tmdb_url += f"&popularity.gte={min_popularity}"
        if selected_genres:
            genre_ids = ",".join(selected_genres)
            tmdb_url += f"&with_genres={genre_ids}"

        # Fetch movies from TMDB API across multiple pages
        movies = fetch_movies_from_tmdb(tmdb_url, num_pages=10)

    # Handle pagination of the filtered movies
    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")

    # Paginate the movies (20 movies per page)
    paginator = Paginator(movies, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "page_obj": page_obj,  # Pass the paginated movies
        "query_params": query_params,  # Pass the query parameters for filtering
    }
    return render(request, "movies/filter_movies.html", context)


# View to add a movie to the user's watchlist
@login_required
def add_to_watchlist(request, tmdb_id):
    # Fetch movie details from TMDB API
    movie_data = get_movie_details(API_KEY, tmdb_id)

    if movie_data:
        # Extract movie details for watchlist
        title = movie_data["title"]
        poster_url = movie_data.get("poster_url", "")
        description = movie_data.get("description", "")
        genre = ", ".join([g["name"] for g in movie_data["genres"]])
        release_date = movie_data.get("release_date", "")
        rating = movie_data.get("vote_average", 0)

        # Check if the movie is already in the user's watchlist
        if not Watchlist.objects.filter(user=request.user, movie_id=tmdb_id).exists():
            # Add the movie to the watchlist
            Watchlist.objects.create(
                user=request.user,
                movie_id=tmdb_id,
                movie_title=title,
                movie_poster=poster_url,
                description=description,
                genre=genre,
                release_date=release_date,
                rating=rating,
            )
            messages.success(request, f"'{title}' has been added to your watchlist.")
        else:
            messages.warning(request, f"'{title}' is already in your watchlist.")
    else:
        messages.error(request, "Failed to retrieve movie details.")

    return redirect("watchlist")


# View to display the user's watchlist
@login_required
def view_watchlist(request):
    # Retrieve all movies in the user's watchlist
    watchlist_movies = Watchlist.objects.filter(user=request.user)
    return render(
        request, "accounts/watchlist.html", {"watchlist_movies": watchlist_movies}
    )


# View to remove a movie from the user's watchlist
@login_required
def remove_from_watchlist(request, movie_id):
    # Remove the movie from the user's watchlist
    Watchlist.objects.filter(user=request.user, movie_id=movie_id).delete()
    messages.success(request, "Movie removed from your watchlist.")
    return redirect("watchlist")


# View to toggle the 'watched' status of a movie in the watchlist
@login_required
def toggle_watched(request, movie_id):
    try:
        # Retrieve the movie from the watchlist
        watchlist_item = Watchlist.objects.get(user=request.user, movie_id=movie_id)
        watchlist_item.watched = (
            not watchlist_item.watched
        )  # Toggle the 'watched' status
        watchlist_item.save()

        # Notify the user of the change
        status = "watched" if watchlist_item.watched else "unwatched"
        messages.success(request, f"'{watchlist_item.movie_title}' marked as {status}.")
    except Watchlist.DoesNotExist:
        messages.error(request, "Movie not found in your watchlist.")

    return redirect("watchlist")  # Redirect to the watchlist view
