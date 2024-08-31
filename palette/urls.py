from django.urls import path
from . import views

urlpatterns = [
    path("", views.color_palette_page, name="color_palette_page"),
    path(
        "get_palettes/",
        views.color_palette_view,
        name="color_palette_view",
    ),
]
