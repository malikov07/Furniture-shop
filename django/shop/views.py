from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, ProductImage, Category, Cart, ColorType, FurnitureStyleType, MaterialType
from .forms import ProductForm
from django.contrib.auth.models import User

class ShopView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        color_choices = ColorType.choices
        style_choices = FurnitureStyleType.choices
        material_choices = MaterialType.choices

        product_name = request.GET.get('product_name') or ''
        category_id = request.GET.get('category')
        min_price = request.GET.get('min_price') or 0
        max_price = request.GET.get('max_price') or 100000000000000
        color = request.GET.get('color') or ''
        material = request.GET.get('material') or ''
        style = request.GET.get('style') or ''

        # Filter products based on parameters
        if product_name:
            products = products.filter(name__icontains=product_name)
        if category_id:
            products = products.filter(categories__category_id=category_id)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if color:
            products = products.filter(color=color)
        if material:
            products = products.filter(material=material)
        if style:
            products = products.filter(style=style)

        context = {
            "products": products,
            "categories": categories,
            "color_choices": color_choices,
            "style_choices": style_choices,
            "material_choices": material_choices,
            "form": request.GET,
        }
        return render(request, "shop/shop.html", context)

class ProductDetailView(LoginRequiredMixin, View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        categories = product.categories.all()
        p_images = product.images.all()
        context = {
            "product": product,
            "p_images": p_images,
            "categories": categories,
        }
        return render(request, "shop/detail.html", context)

# Other views remain unchanged...


class ProductCreateView(View):

    def get(self, request):
        form = ProductForm()
        return render(request, "shop/product_form.html", {"form": form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save()
            if images:
                for image in images:
                    ProductImage.objects.create(product=product, image=image)
            return redirect("shop")
        return render(request, "shop/product_form.html", {"form": form})


class ProductUpdateView(View):

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = ProductForm(instance=product)
        return render(request, "shop/product_form.html", {"form": form})

    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = ProductForm(request.POST, instance=product)
        images = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save()
            if images:
                product.images.all().delete()
                for image in images:
                    ProductImage.objects.create(product=product, image=image)
            return redirect("detail", product.slug)
        return render(request, "shop/product_form.html", {"form": form})


class ProductDeleteView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        return render(request, "shop/product_confirm_delete.html", {"product": product})

    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return redirect("shop")
    
class CartView(View,LoginRequiredMixin):
    def get(self,request):
        print("cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
        carts = Cart.objects.filter(user=request.user)
        context = {
            "carts":carts
        }
        return render(request,"shop/cart.html", context)

class AddToCartView(View, LoginRequiredMixin):
    def get(self, request):
        try:
            user_id = request.GET.get("user_id")
            product_id = request.GET.get("product_id")

            if user_id is None or product_id is None:
                # If either user_id or product_id is missing, return an error response
                return JsonResponse({"error": "Both user_id and product_id are required."}, status=400)

            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.create(user=user, product=product)
            return redirect("cart")
        except (User.DoesNotExist, Product.DoesNotExist):
            # If user or product does not exist, return an error response
            return JsonResponse({"error": "User or product does not exist."}, status=404)
    def post(self,request):
        print("posttttttttttttttttttttttttttttttttttttttt")

# class UpdateCountOfCart(View):
#     def post(self,request):
#         cart_id = request.POST["cart_id"]
#         quantity = request.POST["quantity"]
#         cart = Cart.objects.get(id=cart_id)
#         cart.count = quantity
#         cart.save()
#         return redirect("cart")
    
        
# class DeleteCart(View):
#     def get(self,request):
#         cart_id = request.GET["cart_id"]
#         cart = Cart.objects.get(id=cart_id)
#         cart.delete()
#         return redirect("cart")