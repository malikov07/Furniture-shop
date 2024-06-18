from django import forms
from .models import Product, Category, ProductImage


class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "color",
            "width",
            "height",
            "deep",
            "price",
            "categories",
            "company_name",
            "style",
            "image",
            "material",
            "country",
            "warranty_duration",
            "slug", 
        ]
