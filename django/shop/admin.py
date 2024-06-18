from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product, ProductImage, ProductCategory

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductCategoryInline(admin.StackedInline):
    model = ProductCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display_links = ('id', 'name', 'created_date')
    list_display = ('id', 'name', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('name',)
    ordering = ("id","name",)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'description', 'price','product_image', 'created_date', 'updated_date')
    list_display_links = ('id', 'name', 'description', 'price','product_image', 'created_date', 'updated_date')
    list_filter = ('created_date', 'updated_date')
    search_fields = ('name', 'description')
    readonly_fields = ('created_date', 'updated_date')
    inlines = [ProductImageInline, ProductCategoryInline]
    ordering = ("id","name",)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'slug', 'color', 'width', 'height', 'deep', 'price', 'company_name', 'style', 'image', 'material', 'country', 'watanty_duration')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product', 'image', 'alt_text')
    list_filter = ('product__name', 'alt_text')
    search_fields = ('product__name', 'alt_text')
    ordering = ("id","product",)


@admin.register(ProductCategory)
class ProductCategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product', 'category')
    list_filter = ('id', 'product', 'category')
    search_fields = ('id', 'product', 'category')
    readonly_fields = ('category',)
    ordering = ("id",)
