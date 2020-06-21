from django.contrib import admin
from .models import Category, Item, Label, Specification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['label_name', 'slug']
    prepopulated_fields = {'slug': ('label_name',)}

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['spec_name','width', 'height','depth','weight','quality_checking',
                    'freshness_duration', 'when_packeting', 'each_box_contains']

@admin.register(Item)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price','feature',
                    'available', 'created', 'updated']
    list_filter = ['feature','available', 'created', 'updated']
    list_editable = ['price', 'available', 'feature']
    prepopulated_fields = {'slug': ('name',)}
