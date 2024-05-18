from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from hospital.models import Patient

# Create your models here.
class Nurse(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)  # 저장하기 전에 비밀번호를 해시
        super(Nurse, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # 비밀번호 검증
    
    def __str__(self):
        return self.name

class Record(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    context = models.TextField()
    date = models.DateField(auto_now_add=True)