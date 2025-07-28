from django.contrib import admin
from .models import *

# Register your models here.

class Uploadadmin(admin.ModelAdmin):
    list_display = ['model_name','uploaded_at']
    
admin.site.register(Upload,Uploadadmin)
