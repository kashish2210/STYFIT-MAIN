from django.urls import path
from . import views

app_name = "visual_search"
urlpatterns = [
    # Other URL patterns...
    path("", views.visual_matches_view, name="visual_matches"),
]
