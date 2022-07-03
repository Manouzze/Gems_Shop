from django.contrib import admin
from store.models import Gem
from .models import Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('gem_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('gem_name',)} #Remplie automatiquement le slug

class VariationAdmin(admin.ModelAdmin):
    list_display = ('gem', 'variation_category', 'variation_value', 'is_active', )
    list_editable = ('is_active',)
    list_filter = ('gem', 'variation_category', 'variation_value')



admin.site.register(Gem, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
