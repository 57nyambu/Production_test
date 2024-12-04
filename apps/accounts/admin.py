from django.contrib import admin
from django.http import HttpRequest
from .models import CustomUser

admin.site.register(CustomUser)