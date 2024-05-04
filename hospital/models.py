from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    context = models.TextField()
    drug_list = models.TextField()
    
class drug(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    
