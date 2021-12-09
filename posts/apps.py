from django.apps import AppConfig
# Obłusga wszystkiego co dotyczy postów, komentarzy, wyświetlanie postów oraz ich wyszukiwanie


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
