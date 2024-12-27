from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Insurance, Report,Bill
from .views import insurance

# Register your models here.

admin.site.register(Insurance)
admin.site.register(Bill)
admin.site.register(Report)
