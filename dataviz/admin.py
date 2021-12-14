from django.contrib import admin
from .models import Building, Meter, HalfHourly
# Register your models here.

admin.site.register(Building)
admin.site.register(Meter)
admin.site.register(HalfHourly)

