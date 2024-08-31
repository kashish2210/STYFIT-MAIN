"""
URL configuration for color_palette project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("color_palette/", include("palette.urls")),
    path("visual_search/", include("visual_search.urls")),
    path("clothes/", include("clothes.urls")),
    path("astrochat/", include("astrochat.urls")),
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("tryon/", include("tryon.urls")),
    path("virtual_tailor/", include("virtual_tailor.urls")),
    path("login", views.login, name="login"),
    path("cart", views.cart, name="cart"),
    path("review", views.review, name="review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
