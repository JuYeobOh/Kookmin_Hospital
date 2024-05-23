from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Patient, Prescription, PrescriptionDrug, Drug
from .serializers import PatientSerializer, PrescriptionSerializer, PrescriptionDrugSerializer, DrugSerializer, PrescriptionDrugFlatSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    @action(detail=True, methods=['post'])
    def add_drugs(self, request, pk=None):
        prescription = self.get_object()
        drugs_data = request.data.get('prescription_drugs', [])
    
        for drug_data in drugs_data:
            drug_id = drug_data.pop('drug')
            drug = Drug.objects.get(id=drug_id)
            PrescriptionDrug.objects.create(prescription=prescription, drug=drug, **drug_data)
        return Response({'status': 'drugs added'})
    
    @action(detail=False, methods=['post'], url_path='give_drug')
    @transaction.atomic
    def give_drug(self, request):
        prescription_drugs = PrescriptionDrug.objects.all()
        for pd in prescription_drugs:
            if pd.drug.count < pd.quantity:
                return Response({'error': f'Not enough {pd.drug.name} in stock'}, status=status.HTTP_400_BAD_REQUEST)
            pd.drug.count -= pd.quantity
            pd.drug.save()
        return Response({'status': 'drugs given'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='check_drug')
    def check_drug(self, request):
        prescription_drugs = PrescriptionDrug.objects.all().select_related('prescription__patient', 'drug').order_by('prescription__patient__name', 'drug__name')
        serializer = PrescriptionDrugFlatSerializer(prescription_drugs, many=True)
        return Response(serializer.data)

class PrescriptionDrugViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionDrug.objects.all()
    serializer_class = PrescriptionDrugSerializer

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
