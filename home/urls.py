from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from home import views
from .views import PostUpdateView, PostListView, UserPostListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("Registration/", views.Registration, name="Registration"),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('', include("django.contrib.auth.urls")),

    path('users/', views.users_list, name='users_list'),
    path('users/<slug>/', views.profile_view, name='profile_view'),
    path('friends/', views.friend_list, name='friend_list'),
    path('users/friend-request/send/<int:id>/', views.send_friend_request, name='send_friend_request'),
    path('users/friend-request/cancel/<int:id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('users/friend-request/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    path('users/friend-request/delete/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
    path('users/friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('search_users/', views.search_users, name='search_users'),
    path('', PostListView.as_view(), name='home'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('like/', views.like, name='post-like'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('users_posts/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
