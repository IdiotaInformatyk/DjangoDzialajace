from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comments, Post


class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField()

    # Wykorzystanie podstawki od Django do tworzenia urzytkowników (UserCreationForm)
    # EmailField wykorzystuje EmailValidator zeby sprawdzić poprawność zapisu emailu


# UserRegisterForm — This is for registration of a new user.
# We user the Django’s default UserCreationForm and we define what should be in the forms.
# We set the email to be Django’s EmailField.
# Then we tell Django that model is User and the fields that we would ask the user to fill while registering.


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# UserUpdateForm — This form will let users update their profile.
# It will have all the same fields as Registration form but we would use the Django Model form instead of UserCreationForm.


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# ProfileUpdateForm — This form will let users update their profile.


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

# NewPostForm — This is for posting a new post by any user.
# It takes in three fields namely description, fields and tags.
# user_name is supplied while saving since it is not to be asked to the user.


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'pic', 'tags']

# NewCommentForm — Similar to NewPostForm, we have this form to accept new comments.
# We only take in the comment to be posted and supply the post and the user later.


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
