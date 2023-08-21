from django.db import models
from home.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)


class AdvisorProductLink(models.Model):
    advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_advisor")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    link = models.CharField(max_length=200, unique=True)
