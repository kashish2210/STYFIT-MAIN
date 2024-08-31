from django.urls import path
from . import views

urlpatterns = [
    path("", views.noopath, name="noopath"),
    path("register", views.register_cloth, name="register_cloth"),
    path("registered", views.cloth_registered, name="cloth_registered"),
    path("list/", views.list_clothes, name="list_clothes"),
    path("sell_cloth/", views.sell_cloth, name="sell_cloth"),
    path(
        "sale_result/<int:sale_id>/", views.cloth_sale_result, name="cloth_sale_result"
    ),
]
