from django.contrib import admin
from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):# Sert à modifier l'affichage dans l'interface d'adminitration
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug') #Remplie automatiquement le slug avec le nom de la categorie

admin.site.register(Category, CategoryAdmin)