from django.contrib import admin
from .models import Profile
# Register your models here.

# oznacza modele które zostaną zarejestrowane do naszego panelu administracyjnego
admin.site.register(Profile)