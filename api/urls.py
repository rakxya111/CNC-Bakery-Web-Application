from django.urls import path
from .views import (
    ProductListView,
    CustomizationOptionListView,
    ProductCustomizationCreateView,
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('options/', CustomizationOptionListView.as_view(),name='options'),
    path('customizations/', ProductCustomizationCreateView.as_view(), name='customization-create'),
]