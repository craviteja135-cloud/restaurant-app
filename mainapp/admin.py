from django.contrib import admin
from .models import Contact, MenuItem, Reservation

# Register your models here.

admin.site.register(Contact)
admin.site.register(MenuItem)
admin.site.register(Reservation)
