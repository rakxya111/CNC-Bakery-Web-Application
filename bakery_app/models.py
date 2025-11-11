from django.db import models

# Create your models here.


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d',blank=False)

    def __str__(self):
        return self.product_name
    

class CustomizationOption(models.Model):
    CATEGORY_CHOICES = [
        ('base', 'Base'),
        ('size', 'Size'),
        ('filling', 'Filling'),
        ('flavor', 'Flavor'),
        ('decor','Decor'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    extra_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.category} - {self.name}" 
    

class ProductCustomization(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    base = models.ForeignKey(CustomizationOption , on_delete=models.SET_NULL, null=True, related_name='base_customizations')
    size = models.ForeignKey(CustomizationOption, on_delete=models.SET_NULL,null=True, related_name='size_customizations')
    filling = models.ForeignKey(CustomizationOption, on_delete=models.SET_NULL,null=True, related_name='filling_customizations')
    flavor = models.ForeignKey(CustomizationOption, on_delete=models.SET_NULL, null=True, related_name='flavor_customizations')
    decor = models.ForeignKey(CustomizationOption, on_delete=models.SET_NULL, null=True, related_name='decor_customizations')
    message = models.CharField(max_length=200, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def calculate_total(self):
        base_price = self.product.price
        extras = sum([
            (self.base.extra_price if self.base else 0),
            (self.size.extra_price if self.size else 0),
            (self.filling.extra_price if self.filling else 0),
            (self.flavor.extra_price if self.flavor else 0),
            (self.decor.extra_price if self.decor else 0)
        ])
        return base_price + extras
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Customization for {self.product.product_name} - {self.total_price}"







   