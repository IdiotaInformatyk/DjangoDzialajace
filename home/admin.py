from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile, FriendRequest, Post, Comments, Like

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Like)
