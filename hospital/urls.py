from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('drug_list', views.drug_list, name='drug_list'),
    path('patient_list', views.patient_list, name='patient_list'),
    path('patient/<int:patient_id>', views.patient_detail, name='patient_detail'),
]
