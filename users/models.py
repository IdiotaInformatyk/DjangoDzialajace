from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    # przy usunięciu uzytkownika usuwamy równiez Profil
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # przechowywanie zdjęcia
    image = models.ImageField(default='default.png', upload_to='prof_pic')

    slug = AutoSlugField(populate_from='user')

    # Wyświetla nazwę uzytkownika jako obiekt zapytania

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)