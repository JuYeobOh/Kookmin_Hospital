from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    context = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
class Drug(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField()
    def __str__(self):
        return self.name

class PrescriptionDrug(models.Model):
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, related_name='prescription_drugs')
    drug = models.ForeignKey('Drug', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.drug.name} - {self.quantity}"

