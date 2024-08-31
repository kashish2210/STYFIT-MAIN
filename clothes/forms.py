from django import forms
from .models import Cloth


class ClothForm(forms.ModelForm):
    class Meta:
        model = Cloth
        fields = [
            "title",
            "description",
            "price",
            "size",
            "material",
            "discount_rate",
            "gender",
            "brand",
            "image",
        ]

    def clean_discount_rate(self):
        discount_rate = self.cleaned_data.get("discount_rate")
        if discount_rate > 100:
            raise forms.ValidationError("Discount rate cannot exceed 100.")
        return discount_rate

    def clean_image(self):
        image = self.cleaned_data.get("image")
        # Ensure the image file is valid
        if image and not image.name.lower().endswith(("png", "jpg", "jpeg", "gif")):
            raise forms.ValidationError(
                "Invalid image format. Supported formats: PNG, JPG, JPEG, GIF."
            )
        return image
