from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def virtual_tailor(request):
    return render(request, "virtual_tailor.html")


def vtform(request):
    return HttpResponse("Order placed!")
