from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    context = models.TextField()
    drugs = models.ManyToManyField('Drug')
    
class Drug(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    
class HealthcareManager:

    def create_patient(self, name, age):
        """환자 생성"""
        patient = Patient(name=name, age=age)
        patient.save()
        return patient

    def create_drug(self, name, count):
        """약품 생성"""
        drug = Drug(name=name, count=count)
        drug.save()
        return drug

    def create_prescription(self, patient_id, context, drug_ids):
        """처방전 생성 및 약품 연결"""
        patient = Patient.objects.get(id=patient_id)
        prescription = Prescription(patient=patient, context=context)
        prescription.save()
        for drug_id in drug_ids:
            drug = Drug.objects.get(id=drug_id)
            prescription.drugs.add(drug)
        return prescription

    def add_drug_count(self, drug_id, count):
        """약품 수량 업데이트"""
        drug = Drug.objects.get(id=drug_id)
        drug.count += count
        drug.save()

    def get_patient(self, patient_id):
        """특정 환자 조회"""
        return Patient.objects.get(id=patient_id)

    def get_patient_prescriptions(self, patient_id):
        """특정 환자의 모든 처방전 조회"""
        return Prescription.objects.filter(patient__id=patient_id)