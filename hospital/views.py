from django.shortcuts import render
from .models import HealthcareManager, Patient, Prescription, Drug

# Create your views here.
def index(request):
    return render(request, 'hospital/index.html')

def drug_list(request):
    drug_list = Drug.objects.all()
    context = {drug_list: drug_list}
    return render(request, 'hospital/drug_list.html', context)

def patient_list(request):
    patient_list = Patient.objects.all()
    context = {patient_list: patient_list}
    return render(request, 'hospital/patient_list.html', context)

def patient_detail(request, patient_id):
    if request.method == 'POST':
        context = request.POST.get('context')
        drug_ids = request.POST.getlist('drug_ids')
        HealthcareManager.create_prescription(patient_id, context, drug_ids)
    else:
        patient = HealthcareManager.get_patient(patient_id)
        prescriptions = HealthcareManager.get_patient_prescriptions(patient_id)
        context = {patient: patient, prescriptions: prescriptions}
        return render(request, 'hospital/patient_detail.html', context)