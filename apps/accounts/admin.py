from django.contrib import admin
from .models import CustomUser

# Register CustomUser model in the admin panel
admin.site.register(CustomUser)
