from django.urls import path
from . import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("<int:tmdb_id>/", views.movie_detail, name="movie_detail"),
    path("trending/", views.trending_movies, name="trending_movies"),
    path("random/", views.show_movies, name="movies_random"),
    path("filter/", views.filter_movies, name="filter_movies"),
    path("search/", views.movie_search, name="movie_search"),
    path(
        "add-to-watchlist/<str:tmdb_id>/",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
    path("watchlist/", views.view_watchlist, name="watchlist"),
    path(
        "remove-from-watchlist/<int:movie_id>/",
        views.remove_from_watchlist,
        name="remove_from_watchlist",
    ),
    path("toggle-watched/<int:movie_id>/", views.toggle_watched, name="toggle_watched"),
    path("review/delete/<int:review_id>/", views.delete_review, name="delete_review"),
]
