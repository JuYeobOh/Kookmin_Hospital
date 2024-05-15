# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NurseViewSet, RecordViewSet

router = DefaultRouter()
router.register(r'nurses', NurseViewSet, basename='nurse')
router.register(r'records', RecordViewSet, basename='record')

urlpatterns = [
    path('api/', include(router.urls)),
]
