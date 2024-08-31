from django.shortcuts import render
from django.http import JsonResponse
import random
import google.generativeai as genai
import os
import json

genai.configure(api_key="AIzaSyA2i4KZU4YzGty_GN0-obC07e_ufWPlxdg")

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_color_palette(query):
    prompt = f"""Generate a list which contains 5 list and each of these lists contain 4 colour palettes(i.e color code) related to this word: "{query}". The list have json format. I'm going to use this result in my webapp. So only give the list nothing else, no explain no nothing. you don't need to assign in it in any variable as well. Format should be like this:
[
["color1", "color2", "color3", "color4"],
["color1", "color2", "color3", "color4"],
["color1", "color2", "color3", "color4"],
["color1", "color2", "color3", "color4"],
["color1", "color2", "color3", "color4"]
]"""
    response = model.generate_content(prompt)
    return response.text


def color_palette_view(request):
    if request.method == "GET":
        query = request.GET.get("query", "")
        color_palettes = generate_color_palette(query)
        return JsonResponse(json.loads(color_palettes), safe=False)


def color_palette_page(request):
    return render(request, "color_palettes.html")
