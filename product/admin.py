from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from product.models import Category, Product, Images, Comment


class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class ProductAdmin(admin.ModelAdmin):
     list_display = ['title', 'category', 'price', 'coverType', 'publisher', 'image_tag', 'amount']
     list_filter = ['status']
     inlines = [ProductImageInline]
     readonly_fields = ('image_tag',)
     prepopulated_fields = {'slug': ('title',)}

class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'image_tag']
    list_filter = ['title']
    readonly_fields = ('image_tag',)
from django.utils.html import format_html

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title', )}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'amount',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.amount
    related_products_count.short_description = 'İlgili ürünler (bu kategori için)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'İlgili ürünler (ağaçtaki)'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'product', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
