from rest_framework import generics, viewsets, status
from rest_framework.response import Response 
from bakery_app.models import Product, CustomizationOption, ProductCustomization  
from cart.models import Cart, CartItem
from .serializers import (
    ProductSerializer,
    CustomizationOptionSerializer,
    ProductCustomizationSerializer,
    CartSerializer,
    CartItemSerializer,
)

# =================== PRODUCT VIEWS ==========================


class ProductListView(generics.ListAPIView):
    """
    Returns list of all available products
    """
    queryset = Product.objects.filter(is_available=True)  
    serializer_class = ProductSerializer

# Returns all customization options
class CustomizationOptionListView(generics.ListAPIView):
    queryset = CustomizationOption.objects.all()
    serializer_class = CustomizationOptionSerializer

    def get_queryset(self):
        # Allow filtering by category
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

# Create a new product customization
class ProductCustomizationCreateView(generics.CreateAPIView):
    queryset = ProductCustomization.objects.all()
    serializer_class = ProductCustomizationSerializer



# =================== CART VIEWS ==========================



# Cart ViewSet - Handles all cart opeartions
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'cart_id' # use cart_id instead of default 'pk'

    def create(self,request,*args,**kwargs):
        # Create a new empty Cart
        cart = Cart.objects.create()
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# CartItem ViewSet -: Handles cart Item Opeartions

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self,request,*args,**kwargs):
        # Add item to cart 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    