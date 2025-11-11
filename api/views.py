from rest_framework import generics
from bakery_app.models import Product, CustomizationOption, ProductCustomization
from .serializers import (
    ProductSerializer,
    CustomizationOptionSerializer,
    ProductCutomizationSerializer,
)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomizationOptionListView(generics.ListAPIView):
    queryset = CustomizationOption.objects.all()
    serializer_class = CustomizationOptionSerializer


class ProductCustomizationCreateView(generics.CreateAPIView):
    queryset = ProductCustomization.objects.all()
    serializer_class = ProductCutomizationSerializer
