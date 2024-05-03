from django import forms
from shop.models import ProductModel

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = [
            "category",
            "title",
            "slug",
            "description",
            "brief_description",
            "status",
            "discount_pecent",
            "price",
            "image",
            "stock",
        ]