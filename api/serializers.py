from rest_framework import serializers
from bakery_app.models import Product, CustomizationOption, ProductCustomization  # Fixed import
from cart.models import Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product - Converts Product model to JSON
    """
    class Meta:
        model = Product
        fields = '__all__'  

class CustomizationOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomizationOption - Shows available customization choices
    """
    class Meta:
        model = CustomizationOption
        fields = '__all__'


# Serializer for ProductCustomization - Handles both reading and writing
class ProductCustomizationSerializer(serializers.ModelSerializer):
    # For READING (GET requests) - show full details
    base = CustomizationOptionSerializer(read_only=True)
    size = CustomizationOptionSerializer(read_only=True)
    filling = CustomizationOptionSerializer(read_only=True)
    flavor = CustomizationOptionSerializer(read_only=True)
    decor = CustomizationOptionSerializer(read_only=True)
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    # For WRITING (POST requests) - accept IDs
    base_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomizationOption.objects.filter(category='base'),
        source='base',
        write_only=True,
        required=False,
        allow_null=True
    )
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomizationOption.objects.filter(category='size'),
        source='size',
        write_only=True,
        required=False,
        allow_null=True
    )
    filling_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomizationOption.objects.filter(category='filling'),
        source='filling',
        write_only=True,
        required=False,
        allow_null=True
    )
    flavor_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomizationOption.objects.filter(category='flavor'),
        source='flavor',
        write_only=True,
        required=False,
        allow_null=True
    )
    decor_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomizationOption.objects.filter(category='decor'), 
        source='decor',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProductCustomization
        fields = [
            'id', 'product', 'product_name', 
            'base', 'base_id',
            'size', 'size_id',
            'filling', 'filling_id',
            'flavor', 'flavor_id',
            'decor', 'decor_id',
            'message', 'total_price'
        ]
        extra_kwargs = {
            'product': {'write_only': False},
            'total_price': {'read_only': True}
        }

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem - Items in the shopping cart
    """
    # For READING - show full customization details
    customization = ProductCustomizationSerializer(read_only=True)
    
    # For WRITING - accept customization ID
    customization_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCustomization.objects.all(),
        source='customization',
        write_only=True
    )
    
    # For WRITING - accept cart ID
    cart_id = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(),
        source='cart',
        write_only=True
    )
    
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'customization', 'customization_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        """Calculate total price for this cart item"""
        return obj.get_total()

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart - The shopping cart with all items
    """
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_id', 'created_at', 'items', 'total']
    
    def get_total(self, obj):
        """Calculate total price of all items in cart"""
        return sum([item.get_total() for item in obj.items.all()])
    
