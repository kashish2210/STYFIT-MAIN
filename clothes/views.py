from django.shortcuts import render, redirect, HttpResponse
from .forms import ClothForm
from .models import Cloth, ClothSale
from django.db.models import Q


material_price_per_gram = {
    "cotton": 0.02,
    "jeans": 0.03,
    "woollen": 0.04,
    "nylon": 0.03,
    "synthetic": 0.02,
    "mix": 0.03,
}


def register_cloth(request):
    if request.method == "POST":
        form = ClothForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cloth_registered")
    else:
        form = ClothForm()

    return render(request, "register_cloth.html", {"form": form})


def cloth_registered(request):
    return render(request, "cloth_registered.html")


def noopath(request):
    return HttpResponse("hello there")


from django.shortcuts import render
from .models import Cloth

from django.shortcuts import render
from .models import Cloth


def list_clothes(request):
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    size = request.GET.get("size")
    search_query = request.GET.get("search_query", "")

    # Base queryset
    clothes = Cloth.objects.all()

    # Apply search filter
    if search_query:
        clothes = clothes.filter(title__icontains=search_query) | clothes.filter(
            description__icontains=search_query
        )

    # Filter by size
    if size:
        clothes = clothes.filter(size=size)

    # Calculate price_after_discount and filter by price range
    filtered_clothes = []
    for cloth in clothes:
        price_after_discount = cloth.price * (1 - cloth.discount_rate / 100)

        # Convert min_price and max_price to floats if they are provided
        try:
            min_price_float = float(min_price) if min_price else None
        except ValueError:
            min_price_float = None

        try:
            max_price_float = float(max_price) if max_price else None
        except ValueError:
            max_price_float = None

        # Filter based on price range
        if (min_price_float is None or price_after_discount >= min_price_float) and (
            max_price_float is None or price_after_discount <= max_price_float
        ):
            cloth.price_after_discount = price_after_discount
            filtered_clothes.append(cloth)

    context = {
        "clothes": filtered_clothes,
        "sizes": ["S", "M", "L", "XL", "XXL", "XXXL"],
    }
    return render(request, "list_clothes.html", context)


def someValueOrDefaultZero(someValue):
    return float(someValue) if someValue else 0


def sell_cloth(request):
    if request.method == "POST":
        # Get the weights from the form, defaulting to 0 if not provided
        cotton_weight = someValueOrDefaultZero(request.POST.get("cotton_weight"))
        jeans_weight = someValueOrDefaultZero(request.POST.get("jeans_weight"))
        woollen_weight = someValueOrDefaultZero(request.POST.get("woollen_weight"))
        nylon_weight = someValueOrDefaultZero(request.POST.get("nylon_weight"))
        synthetic_weight = someValueOrDefaultZero(request.POST.get("synthetic_weight"))
        mix_weight = someValueOrDefaultZero(request.POST.get("mix_weight"))

        # Calculate the total price (using random prices for now)
        cotton_price = (
            cotton_weight * material_price_per_gram["cotton"]
        )  # Random multiplier for example
        jeans_price = jeans_weight * material_price_per_gram["jeans"]
        woollen_price = woollen_weight * material_price_per_gram["woollen"]
        nylon_price = nylon_weight * material_price_per_gram["nylon"]
        synthetic_price = synthetic_weight * material_price_per_gram["synthetic"]
        mix_price = mix_weight * material_price_per_gram["mix"]

        total_price = (
            cotton_price
            + jeans_price
            + woollen_price
            + nylon_price
            + synthetic_price
            + mix_price
        )

        # Save the data to the database
        cloth_sale = ClothSale.objects.create(
            cotton_weight=cotton_weight,
            jeans_weight=jeans_weight,
            woollen_weight=woollen_weight,
            nylon_weight=nylon_weight,
            synthetic_weight=synthetic_weight,
            mix_weight=mix_weight,
            total_price=total_price,
        )

        # Redirect to a new page with the sale info
        return redirect("cloth_sale_result", sale_id=cloth_sale.id)

    return render(request, "sell_cloth.html")


def cloth_sale_result(request, sale_id):
    cloth_sale = ClothSale.objects.get(id=sale_id)
    return render(request, "sale_result.html", {"cloth_sale": cloth_sale})
