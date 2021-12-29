from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comments, Post


class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField()

    # Wykorzystanie podstawki od Django do tworzenia urzytkowników (UserCreationForm)
    # EmailField wykorzystuje EmailValidator zeby sprawdzić poprawność zapisu emailu


# UserRegisterForm — Służy do rejestracji nowego użytkownika.
# Używamy domyślnego UserCreationForm Django i definiujemy, co powinno być w formularzach.
# Ustawiliśmy adres e-mail na EmailField Django.
# Następnie mówimy Django, że model to Użytkownik i pola, które poprosilibyśmy użytkownika o wypełnienie podczas rejestracji.


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# UserUpdateForm — ten formularz pozwoli użytkownikom zaktualizować swój profil.
# Będzie miał wszystkie te same pola, co formularz rejestracyjny, ale zamiast formularza UserCreationForm użyjemy formularza Model Django.

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# ProfileUpdateForm — ten formularz pozwoli użytkownikom zaktualizować swoje profile.


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

# NewPostForm — służy do publikowania nowego posta przez dowolnego użytkownika.
# Zajmuje trzy pola, a mianowicie opis, pola i tagi.
# user_name jest podawana podczas zapisywania, ponieważ nie należy o nią pytać użytkownika.


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'pic', 'tags']


# NewCommentForm — Podobnie jak NewPostForm, mamy ten formularz do przyjmowania nowych komentarzy.
# Bierzemy tylko komentarz do opublikowania i dostarczamy post i użytkownika później.


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
