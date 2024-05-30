from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChemistViewSet

router = DefaultRouter()
router.register(r'chemists', ChemistViewSet, basename='chemist')

urlpatterns = [
    path('api/', include(router.urls)),
]
