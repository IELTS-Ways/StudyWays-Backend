import warnings
from django.apps import AppConfig
from django.core.cache import CacheKeyWarning

warnings.simplefilter("ignore", CacheKeyWarning)

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
