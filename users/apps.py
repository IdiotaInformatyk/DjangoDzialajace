from django.apps import AppConfig


# Aplikacja Users obsłuży wszystkie modele, formularze i widoki dotyczące profili użytkowników, znajomych i
# wysyłania, odbierania próśb, wyszukiwania użytkowników i nawiązywania nowych znajomości


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
