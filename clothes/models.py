from django.db import models


class Cloth(models.Model):
    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
        ("XXL", "Double Extra Large"),
        ("XXXL", "Triple Extra Large"),
    ]

    MATERIAL_CHOICES = [
        ("cotton", "Cotton"),
        ("jeans", "Jeans"),
        ("denim", "Denim"),
        ("woollen", "Woollen"),
        ("nylon", "Nylon"),
        ("synthetic", "Synthetic"),
        ("mix", "Mix"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    brand = models.CharField(max_length=255)
    image = models.ImageField(upload_to="cloth_images/")

    def set_discount(self, percentage):
        self.discount_rate = percentage
        self.save()

    def generate_similar_clothes(self):
        # Implement logic for generating similar clothes
        pass

    def __str__(self):
        return self.title


class ClothSale(models.Model):
    cotton_weight = models.FloatField(default=0.0)
    jeans_weight = models.FloatField(default=0.0)
    woollen_weight = models.FloatField(default=0.0)
    nylon_weight = models.FloatField(default=0.0)
    synthetic_weight = models.FloatField(default=0.0)
    mix_weight = models.FloatField(default=0.0)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"Sale ID {self.id} - Total Price: ${self.total_price:.2f}"
