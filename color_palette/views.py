from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "login.html")


def review(request):
    return render(request, "review.html")


def cart(request):
    return render(request, "cart.html")
