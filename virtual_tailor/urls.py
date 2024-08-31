from django.urls import path
from .views import virtual_tailor, vtform


urlpatterns = [
    path("", virtual_tailor, name="virtual_tailor"),
    path("vtform", vtform, name="vtform"),  # Render the HTML template
]
