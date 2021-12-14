from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path('', views.home, name='home'),
    path("create/", views.create, name="create"),
    path("Registration/", views.Registration, name="Registration"),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('', include("django.contrib.auth.urls")),

]
