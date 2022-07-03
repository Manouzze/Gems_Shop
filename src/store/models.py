from django.db import models
from django.urls import reverse

from category.models import Category

# Create your models here.
class Gem(models.Model):
    gem_name = models.CharField(max_length=100)
    slug = models.SlugField() # moyen d'afficher le champs de notre article dans l'url
    color = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField(blank=True, verbose_name="Contenu")
    images = models.ImageField(upload_to="products", blank=True, null=True)
    stock = models.IntegerField(default=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.gem_name

    def get_url(self):
        return reverse('gem_detail', args=[self.category.slug, self.slug])

class VariationManager(models.Manager):
    def quality(self):
        return super(VariationManager, self).filter(variation_category='quality')
    def carat(self):
        return super(VariationManager, self).filter(variation_category='carat')


variation_category_choice = (
    ('quality', 'quality'),
    ('carat', 'carat'),
)

class Variation(models.Model):
    gem = models.ForeignKey(Gem, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value