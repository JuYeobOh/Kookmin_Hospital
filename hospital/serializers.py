from rest_framework import serializers
from .models import Patient, Prescription, PrescriptionDrug, Drug

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age']

class PrescriptionDrugSerializer(serializers.ModelSerializer):
    prescription = serializers.PrimaryKeyRelatedField(queryset=Prescription.objects.all(), required=False)
    drug = serializers.PrimaryKeyRelatedField(queryset=Drug.objects.all())

    class Meta:
        model = PrescriptionDrug
        fields = ['id', 'prescription', 'drug', 'quantity']

class PrescriptionSerializer(serializers.ModelSerializer):
    prescription_drugs = PrescriptionDrugSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'context', 'date', 'prescription_drugs']

    def create(self, validated_data):
        prescription_drugs_data = validated_data.pop('prescription_drugs', [])
        prescription = Prescription.objects.create(**validated_data)
        for drug_data in prescription_drugs_data:
            drug = drug_data.pop('drug')
            PrescriptionDrug.objects.create(prescription=prescription, drug=drug, **drug_data)
        return prescription

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prescription_drugs'] = PrescriptionDrugSerializer(instance.prescription_drugs.all(), many=True).data
        return representation

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
