import requests
import random

API_KEY = "524f4dca187519c13ea9115fa81aebd2"  # Your API key for accessing TMDB API

# URL to fetch popular movies from TMDB
TMDB_POPULAR_URL = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"


# Function to fetch trending movies from TMDB API
def get_trending_movies(api_key, language="en-US", pages=5):
    base_url = "https://api.themoviedb.org/3/trending/movie/week"  # API endpoint for weekly trending movies
    image_base_url = (
        "https://image.tmdb.org/t/p/w500"  # Base URL for images with width 500px
    )
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",  # Using Bearer token for authorization
    }
    movies = []

    # Loop through the number of pages specified (default: 5)
    for page in range(1, pages + 1):
        # Construct the request URL with pagination and language settings
        url = f"{base_url}?language={language}&page={page}"
        response = requests.get(url, headers=headers)

        # If the API call is successful, process the results
        if response.status_code == 200:
            results = response.json().get(
                "results", []
            )  # Fetch results list from the response
            for movie in results:
                # Collect the necessary movie data for each movie
                movie_data = {
                    "id": movie.get("id"),  # Movie ID
                    "title": movie.get("title"),  # Movie title
                    "release_date": movie.get("release_date"),  # Release date
                    "vote_average": movie.get("vote_average"),  # Average rating
                    "poster_url": (
                        f"{image_base_url}{movie.get('poster_path')}"
                        if movie.get("poster_path")
                        else None
                    ),
                    # Movie poster URL
                }
                movies.append(movie_data)
        else:
            print(f"Failed to retrieve page {page}: {response.status_code}")
            break  # Stop fetching pages if there's an error in the response

    return movies  # Return the list of movies


# Function to fetch random trending movies from TMDB API
def get_random_movies(api_key, language="en-US", pages=5):
    base_url = "https://api.themoviedb.org/3/trending/movie/week"  # API endpoint for weekly trending movies
    image_base_url = (
        "https://image.tmdb.org/t/p/w500"  # Base URL for images with width 500px
    )
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",  # Authorization token
    }
    all_movies = []

    # Fetch movies from multiple pages
    for page in range(1, pages + 1):
        url = f"{base_url}?language={language}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json().get("results", [])
            for movie in results:
                movie_data = {
                    "id": movie.get("id"),  # Movie ID
                    "title": movie.get("title"),  # Movie title
                    "release_date": movie.get("release_date"),  # Release date
                    "vote_average": movie.get("vote_average"),  # Average rating
                    "poster_url": (
                        f"{image_base_url}{movie.get('poster_path')}"
                        if movie.get("poster_path")
                        else None
                    ),
                    # Movie poster URL
                }
                all_movies.append(movie_data)
        else:
            print(f"Failed to retrieve page {page}: {response.status_code}")
            break

    # Select 6 random movies from the list if available
    if len(all_movies) >= 6:
        all_movies = random.sample(all_movies, 6)  # Randomly sample 6 movies

    return all_movies  # Return the list of random movies


# Function to get details of a specific movie from TMDB API
def get_movie_details(api_key, movie_id):
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"  # API endpoint for movie details
    image_base_url = (
        "https://image.tmdb.org/t/p/w500"  # Base URL for images with width 500px
    )
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",  # Authorization token
    }

    url = f"{base_url}?api_key={api_key}"  # Complete URL for API request
    response = requests.get(url, headers=headers)

    # If the API call is successful, process the movie data
    if response.status_code == 200:
        movie_data = response.json()  # Convert the response to JSON
        movie = {
            "tmdb_id": movie_data.get("id"),  # TMDB movie ID
            "title": movie_data.get("title"),  # Movie title
            "release_date": movie_data.get("release_date"),  # Release date
            "vote_average": movie_data.get("vote_average"),  # Average rating
            "poster_url": (
                f"{image_base_url}{movie_data.get('poster_path')}"
                if movie_data.get("poster_path")
                else None
            ),
            # Poster URL
            "description": movie_data.get("overview"),  # Movie overview/description
            "genres": movie_data.get("genres", []),  # Genres associated with the movie
        }
        return movie  # Return movie data as a dictionary
    else:
        print(f"Failed to retrieve movie {movie_id}: {response.status_code}")
        return None  # Return None if the API request fails


# Function to fetch available movie genres from TMDB API
def get_genres():
    """Fetches the available movie genres from TMDB API"""
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"  # API endpoint for genres list
    response = requests.get(url)
    result = []

    if response.status_code == 200:
        data = response.json()
        genres = data.get("genres", [])
        # Map genre ID and name into a tuple list
        result = [(genre["id"], genre["name"]) for genre in genres]

    return result  # Return a list of (id, name) tuples representing genres


# Function to fetch movies from multiple pages of TMDB API
def fetch_movies_from_tmdb(tmdb_url, num_pages=10):
    """Fetch movies from multiple pages of the TMDB API."""
    movies = []

    # Loop through the number of pages specified (default: 10)
    for page in range(1, num_pages + 1):
        response = requests.get(f"{tmdb_url}&page={page}")
        if response.status_code != 200:
            break  # Stop if the response is not successful
        data = response.json()
        # Add results (movies) from each page to the list
        movies.extend(data.get("results", []))

    return movies  # Return the list of movies fetched
