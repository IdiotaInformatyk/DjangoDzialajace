# Dodawanie  co zapisać w bazie danych i definiowanie relacje między różnymi modelami i jakie mają cechy
# Create your models here.
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save

# Tak więc naszym pierwszym modelem jest model Profile.
# Ma pięć parametrów:-
# user — jest to relacja jeden do jednego z modelem użytkownika Django. On_delete=models.CASCADE oznacza, że ​​po usunięciu Użytkownika niszczymy również Profil.
# image — w tym miejscu zostanie zapisane zdjęcie profilowe użytkownika. Udostępniliśmy również domyślny obraz. Musimy określić, gdzie zapiszemy zdjęcia.
# slug — To będzie pole slug. Używamy AutoSlugField i ustawiamy go tak, aby robił ślimak z
# pole użytkownika.
# bio — W tym miejscu będzie przechowywane małe wprowadzenie o użytkowniku. Tutaj puste=True oznacza, że ​​można je pozostawić
# pusty.
# friends — to jest model pola wiele do wielu z profilem i można go zostawić puste. Oznacza to, że każdy użytkownik może:
# mieć wielu znajomych i być przyjaciółmi wielu osób. Następnie opisujemy __str__, który decyduje o tym, jak Django
# pokaże nasz model w panelu administracyjnym. Ustawiliśmy go tak, aby wyświetlał nazwę użytkownika jako obiekt zapytania. Definiujemy również
# get_absolute_url, aby uzyskać bezwzględny adres URL dla tego profilu. Następnie definiujemy funkcję, dzięki której profil zostanie utworzony tak szybko, jak
# tworzymy użytkownika, aby użytkownik nie musiał ręcznie tworzyć profilu


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user')
    bio = models.CharField(max_length=255, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/home/{}".format(self.slug)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

# Następnie definiujemy nasz Model Friends. Będzie miał trzy parametry:-
# to_user — Oznacza użytkownika, do którego zostanie wysłana prośba o dodanie do znajomych. Będzie miał ten sam parametr on_delete, który decyduje o usunięciu użytkownika, usuwamy również zaproszenie do znajomych.
# from_user — Oznacza użytkownika, który wysyła zaproszenie do znajomych. Zostanie on również usunięty, jeśli użytkownik zostanie usunięty.
# znacznik czasu — tak naprawdę nie trzeba dodawać. Przechowuje czas wysłania żądania.

class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

# Post model.
# Będzie miał pięć parametrów:-
# description — jest to część posta, w której użytkownik umieściłby krótki opis związany z publikowanym zdjęciem.
# Jest to opcjonalne, ponieważ nie chcemy zmuszać użytkownika do umieszczania opisu.
# Ma maksymalną długość 255 znaków i jest CharField.

# pic — To najważniejsza część wpisu — zdjęcie.
# Użytkownicy prześlą wybrane przez siebie zdjęcie do przesłania.
# Zostanie zapisany we wspomnianej ścieżce do pliku. Używa ImageField.

# date_posted — użyje DateTimeField Django i ustawi znacznik czasu dla każdego posta.
# Użyjemy domyślnego czasu jako czasu bieżącego.

# user_name — to jest relacja klucza obcego.
# Jest to relacja wiele do jednego, ponieważ użytkownik może mieć wiele postów, ale post może należeć tylko do jednego użytkownika.
# Kiedy użytkownik zostanie usunięty, post również zostanie usunięty, o czym świadczy użycie on_delete=models.CASCADE.
# Łączy post z modelem użytkownika.

# tags — służy do pobierania odpowiednich tagów dla posta.
# Może pozostać puste i może mieć maksymalnie 100 znaków.
# Tagi mogą pomóc w wyszukiwaniu odpowiednich postów.

# Następnie opisujemy __str__, który decyduje o tym, jak Django pokaże nasz model w panelu administracyjnym.
# Ustawiliśmy go tak, aby wyświetlał opis jako obiekt zapytania.
# Definiujemy również get_absolute_url, aby uzyskać bezwzględny adres URL dla tego postu.


class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    pic = models.ImageField(upload_to='path/to/img')
    date_posted = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# Następnie mamy model Komentarze. Ma cztery parametry:-

# post — jest to klucz obcy, który łączy post i komentarz.
# Komentarz może dotyczyć jednego posta, ale jeden post może zawierać wiele komentarzy.
# Usunięcie posta spowoduje również usunięcie komentarzy.

# username — jest to klucz obcy, który łączy komentarz z użytkownikiem.
# Gdy użytkownik zostanie usunięty, komentarz również zostanie usunięty.

# comment — To jest CharField, w którym będzie przechowywany odpowiedni komentarz.
# Maksymalny limit znaków to 255 znaków.

# comment_date — użyje DateTimeField Django i ustawi znacznik czasu dla każdego komentarza.
# Użyjemy domyślnego czasu jako czasu bieżącego.


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)

# user — reprezentuje użytkownika, który polubił post.
# Usunięcie użytkownika usuwa podobne.

# post — jest to post, do którego następuje polubienie.
# Usunięcie posta powoduje również usunięcie wszystkich jego polubień.


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)