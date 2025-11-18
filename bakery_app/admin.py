from django.contrib import admin
from .models import Product , CustomizationOption, ProductCustomization

# Register your models here.
admin.site.register(Product)
admin.site.register(CustomizationOption)
admin.site.register(ProductCustomization)
