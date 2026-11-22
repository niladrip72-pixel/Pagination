from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("retrieve/", views.retrieve_posts, name="retrieve_posts"),
    path("posts/", views.all_posts, name="all_posts"),
    path("search/", views.search_post, name="search_post"),
]
