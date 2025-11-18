from django.db import models
from bakery_app.models import ProductCustomization
import uuid


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.cart_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    customization = models.ForeignKey(ProductCustomization, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.customization.total_price * self.quantity
    
    def __str__(self):
        return f"{self.customization.product_name} × {self.quantity}"



