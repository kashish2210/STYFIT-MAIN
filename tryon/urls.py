# urls.py
from django.urls import path
from .views import (
    webcam_feed,
    webcam_page,
    customize3d,
    tryon3d,
    webcam_feed3d,
    measurement_page,
    measurement_feed,
)

urlpatterns = [
    path("webcam/", webcam_page, name="webcam_page"),  # Render the HTML template
    path("webcam_feed/", webcam_feed, name="webcam_feed"),
    path(
        "webcam_feed3d/", webcam_feed3d, name="webcam_feed3d"
    ),  # Provide the webcam feed
    path("customize3d", customize3d, name="customize3d"),
    path("3d", tryon3d, name="tryon3d"),
    path("measurement_page", measurement_page, name="measurement_page"),
    path("measurement_feed", measurement_feed, name="measurement_feed"),
]
