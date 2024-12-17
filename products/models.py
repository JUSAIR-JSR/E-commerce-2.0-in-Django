from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    # Remove the rating field from here
    # rating = models.FloatField()

    def __str__(self):
        return self.name

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.score})"
