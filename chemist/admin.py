from django.contrib import admin
from .models import Chemist

@admin.register(Chemist)
class Chemist(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'age')
    search_fields = ('email', 'name')
