from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)

from product.views import ProductViewSet
from kit.views import KitViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='Product')
router.register(r'kits', KitViewSet, basename='Kit')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('v1/signin/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('v1/signin/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
]
