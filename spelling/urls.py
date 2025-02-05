from .views import Spelling
from django.urls import path

urlpatterns = [
    path("spelling-drills", Spelling.as_view(), name="spelling-drills")
]
