from django.shortcuts import render, HttpResponse
import json
from serpapi import GoogleSearch
import time
import requests


# def visual_matches_view(request):
# # Example JSON string to be replaced with actual API call or file reading
# with open(
#     r"C:\Users\Admin\Desktop\colorP\color_palette\visual_search\api.json",
#     "r",
#     encoding="utf-8",
# ) as f:
#     data = json.load(f)

# # Load JSON data
# visual_matches = data["visual_matches"]

# return render(request, "visual_matches.html", {"visual_matches": visual_matches})


def visual_matches_view(request):
    visual_matches = []

    if request.method == "POST":
        # Check if an image file is uploaded
        if "image_file" in request.FILES:
            image_file = request.FILES["image_file"]

            api = "https://api.imgur.com/3/image"

            params = dict(client_id="546c25a59c58ad7")

            files = dict(
                image=(None, image_file),
                name=(None, ""),
                type=(None, "raw"),
            )

            r = requests.post(api, files=files, params=params)
            image_url = r.json()["data"]["link"]
            time.sleep(2)

            try:
                if image_url:

                    ############### Uncomment below block1 for real demonstration #######################
                    # params = {
                    #     "engine": "google_lens",
                    #     "url": image_url,
                    #     "api_key": f"{os.environ['SerpAPI']}",
                    #     "output": "html",
                    # }

                    # search = GoogleSearch(params)

                    # results = search.get_dict()
                    # visual_matches = results["visual_matches"]

                    ###############  block1 ends ##################

                    ###########When you uncomment above block1 comment this block2 ##################
                    with open(
                        r"C:\Users\Admin\Desktop\colorP\color_palette\visual_search\api.json",
                        "r",
                        encoding="utf-8",
                    ) as f:
                        data = json.load(f)

                    # Load JSON data
                    visual_matches = data["visual_matches"]

                    ############## block2 ends ##############################

            except json.decoder.JSONDecodeError:
                print("Error occured.")

    return render(request, "visual_matches.html", {"visual_matches": visual_matches})


# def visual_matches_view(request):
#     visual_matches = []
#     try:
#         if request.method == "POST":
#             # Assuming you get the image URL from the POST data
#             image_url = request.POST.get("image_url")

#             if image_url:
#                 # params = {
#                 #     "engine": "google_lens",
#                 #     "url": image_url,
#                 #     "api_key": "66000601dd8dc23cde427a4a1ea0f20bab906f019dc7eb33ff499048e89f3f8b",
#                 #     "output": "html",
#                 # }

#                 # search = GoogleSearch(params)

#                 # results = search.get_dict()
#                 # visual_matches = results["visual_matches"]

#                 time.sleep(2)
#                 with open(
#                     r"C:\Users\Admin\Desktop\colorP\color_palette\visual_search\api.json",
#                     "r",
#                     encoding="utf-8",
#                 ) as f:
#                     data = json.load(f)

#                 # Load JSON data
#                 visual_matches = data["visual_matches"]
#     except json.decoder.JSONDecodeError:
#         print("Error occured.")

#     return render(request, "visual_matches.html", {"visual_matches": visual_matches})
