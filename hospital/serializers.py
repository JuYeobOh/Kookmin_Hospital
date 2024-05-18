from rest_framework import serializers
from .models import Patient, Prescription, PrescriptionDrug, Drug

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age']

class PrescriptionDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionDrug
        fields = ['id', 'prescription', 'drug', 'quantity']

class PrescriptionSerializer(serializers.ModelSerializer):
    prescription_drugs = PrescriptionDrugSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'context', 'date', 'prescription_drugs']

    def create(self, validated_data):
        prescription_drugs_data = self.initial_data.get('prescription_drugs')
        prescription = Prescription.objects.create(**validated_data)
        for drug_data in prescription_drugs_data:
            PrescriptionDrug.objects.create(prescription=prescription, **drug_data)
        return prescription

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'name', 'count']

class PrescriptionDrugFlatSerializer(serializers.ModelSerializer):  
    patient = serializers.CharField(source='prescription.patient.name')
    drug = serializers.CharField(source='drug.name')
    class Meta:
        model = PrescriptionDrug
        fields = ['patient', 'drug', 'quantity']