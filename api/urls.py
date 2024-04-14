from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('materials', views.MaterialViewSet)
router.register('product-materials', views.ProductMaterialViewSet)
router.register('partial-warehouse', views.PartialWarehouseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product-info', views.product_info)
]