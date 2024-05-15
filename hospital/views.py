# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, Prescription, PrescriptionDrug, Drug
from .serializers import PatientSerializer, PrescriptionSerializer, PrescriptionDrugSerializer, DrugSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    @action(detail=True, methods=['post'])
    def add_drugs(self, request, pk=None):
        prescription = self.get_object()
        drugs_data = request.data.get('prescription_drugs')
        for drug_data in drugs_data:
            PrescriptionDrug.objects.create(prescription=prescription, **drug_data)
        return Response({'status': 'drugs added'})

class PrescriptionDrugViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionDrug.objects.all()
    serializer_class = PrescriptionDrugSerializer

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
