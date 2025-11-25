from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ImageGallery

class ProductImageInline(admin.TabularInline):
    model = ImageGallery
    extra = 2
    readonly_fields = ('preview',)
    fields = ('image', 'preview',)

    def preview(self, obj):
        if obj and getattr(obj, 'image', None):
            try:
                return mark_safe(f'<img src="{obj.image.url}" style="height:60px;border-radius:4px;" />')
            except Exception:
                return ""
        return ""
    preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'stock', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'thumb')
    readonly_fields = ('thumb',)

    def thumb(self, obj):
        if obj and getattr(obj, 'image', None):
            try:
                return mark_safe(f'<img src="{obj.image.url}" style="height:60px;" />')
            except Exception:
                return ""
        return ""
    thumb.short_description = "Thumbnail"
