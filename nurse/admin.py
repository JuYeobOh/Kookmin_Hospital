from django.contrib import admin
from .models import Nurse, Record

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'age')
    search_fields = ('email', 'name')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'nurse', 'context', 'date')
    search_fields = ('nurse__name', 'context')
    list_filter = ('date',)
