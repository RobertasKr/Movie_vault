# 🎬 Movie Vault
Movie Vault is a web application built using Django that allows users to explore movies, manage their watchlist, write reviews, and more. The application integrates with The Movie Database (TMDB) API to fetch details about trending movies, and it provides an interactive and user-friendly interface for movie enthusiasts.

# 🎥 Features
- User Authentication: Users can register, log in, change their password, and manage their account settings.
- Watchlist Management: Users can add or remove movies to/from their watchlist, and mark movies as watched or unwatched.
- Review System: Users can leave reviews for movies and view reviews left by others.
- Search Functionality: Users can search for movies or TV shows using keywords.
- Trending Movies: A homepage showcasing movies trending today.
- Filtering Movies: Users can filter movies based on rating, release year, genre, and popularity.
- Admin Panel: Superusers can manage content through the built-in Django admin panel.
- Contact Page: Users can submit feedback or inquiries, and admins can view submissions.

# 🛠️ Technology Stack
- Backend: Django 5.1 (Python)
- Frontend: HTML5, CSS3, Bootstrap 5
- Database: SQLite3 (default with Django)
- API Integration: The Movie Database (TMDB) API
- Version Control: Git, GitHub

# 📦 Installation and Setup
Prerequisites:
- Python 3.10 or higher
- Pip
- A TMDB API key

Steps:

Clone the Repository:
git clone https://github.com/your-username/movie_vault.git
cd movie_vault

Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

Configure Environment Variables: Create a .env file in the project root and add the following keys:
TMDB_API_KEY=your_tmdb_api_key_here
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password

Run Migrations:
python manage.py migrate

Create a Superuser: To access the Django admin panel, create a superuser account:
python manage.py createsuperuser

Run the Development Server:
python manage.py runserver

Open your browser and visit http://127.0.0.1:8000/ to see the application.

# 🔑 Key Features and Functionality
User Registration and Authentication:
- Users can create accounts, log in, and manage their profiles.
- Change passwords with the CustomPasswordChangeForm.

Movie Watchlist:
- Users can add movies to their personal watchlist.
- Toggle between watched and unwatched states for movies.

Movie Reviews:
- Logged-in users can write, edit, and delete reviews for movies.
- View all reviews for each movie on its detail page.

Movie Search:
- Search functionality powered by the TMDB API, allowing users to find movies by keywords.

Admin Panel:
- Admins can manage users, movies, and reviews directly through the Django admin interface.

# 🚀 API Integration
The project uses The Movie Database (TMDB) API to fetch movie data like:
- Trending movies
- Movie details (rating, genre, release date, description, etc.)
- Search results
To interact with TMDB, the project utilizes the api_services.py module, which contains helper functions such as get_movie_details, get_trending_movies, and get_random_movies.

# 🔧 Configuration
TMDB API Key
To fetch movie data, you must obtain an API key from TMDB and add it to your environment variables or directly in the settings.

Email Service
The project uses Gmail as the default email service for the contact form. You can change the email service provider in the settings.py file under the EMAIL_BACKEND settings. Make sure to configure your SMTP settings correctly.

# ⚙️ Django Admin
To access the Django admin interface:

- Run the development server and navigate to /admin/.
- Log in with the superuser credentials you created earlier.
- From here, you can manage users, movies, reviews, and more.

# 🌟 Acknowledgements
The Movie Database (TMDB) for the API.
Django framework for the robust backend support.
