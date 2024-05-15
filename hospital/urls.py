from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, PrescriptionViewSet, PrescriptionDrugViewSet, DrugViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'prescription-drugs', PrescriptionDrugViewSet)
router.register(r'drugs', DrugViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
