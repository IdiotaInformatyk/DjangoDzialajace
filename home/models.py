# Dodawanie  co zapisać w bazie danych i definiowanie relacje między różnymi modelami i jakie mają cechy
# Create your models here.
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
#
# So, our first model is the Profile model.
# It has five parameters:-
# user — This is a One to One Relationship with Django User model. The on_delete=models.CASCADE means on the deletion of User, we destroy the Profile too.
# image — This will store the profile picture of the user. We have provided a default image also. We need to define where to
# save the pictures.
# slug — This will be the slug field. We use the AutoSlugField and will set it to make slug from
# the user field.
# bio — This will store the small introduction about the user. Here, blank=True means it can be left
# blank.
# friends — This is a Many to Many Field with Profile model and can be left blank. It means every user can
# have multiple friends and can be friends to multiple people. Next, we describe the __str__ which decides how Django
# will show our model in the admin panel. We have set it to show the username as the Query object. We also define the
# get_absolute_url to get the absolute URL for that profile. Next, we define a function to make a profile as soon as
# we create the user so that the user doesn't have to manually create a profile.


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

# Next, we define our Friends Model. It will have three parameters:-
# to_user — This denotes the user to whom the friend request will be sent. It will have the same on_delete parameter which decides when the user is deleted, we delete the friend request too.
# from_user — This denotes the user who is sending the friend request. It will also be deleted if the user is deleted.
# timestamp — It is not really necessary to add. It stores the time when the request was sent.

class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
# So, let’s have a look at our first model — Post model.
# It will have five parameters:-
# description — This is the part of the post where the user would put a small description relevant to the picture he is posting.
# It is optional since we do not want to force the user to put a description.
# It has a maximum length of 255 characters and is a CharField.

# pic — This is the most important part of the post — the picture.
# Users will upload a picture of their choice for uploading.
# It would be saved in the file path mentioned. It uses an ImageField.

# date_posted — It will use the DateTimeField of Django and will set the timestamp to each post.
# We will use the default time as the current time.

# user_name — This is a ForeignKey relationship.
# It is a Many to One relationship since a user can have many posts but a post can only belong to one user.
# When the user is deleted, the post will be deleted too as evidenced by the usage of on_delete=models.CASCADE.
# It links up the post with the User model.

# tags — This is used to take in relevant tags for the post.
# It can be left blank and is of the maximum of 100 characters.
# Tags can help to search for relevant posts.

# Next, we describe the __str__ which decides how Django will show our model in the admin panel.
# We have set it to show the description as the Query object.
# We also define the get_absolute_url to get the absolute URL for that post.

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

# Next, we have the Comments model. It has four parameters:-

# post — This is a foreign key which connects the post and comment.
# A comment can be for a single post but a single post can have multiple comments.
# Deletion of the post will delete the comments too.

# username — This is a foreign key which relates a comment to the user.
# When the user is deleted, the comment will also be deleted.

# comment — This is the CharField which will hold the relevant comment.
# It has a maximum character limit of 255 characters.

# comment_date — It will use the DateTimeField of Django and will set the timestamp to each comment.
# We will use the default time as the current time.


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)

# user — It represents the user who has liked the post.
# Deleting the user deletes the like.

# post — It is the post on which the like is given.
# Deleting the post deletes all its likes too.


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)