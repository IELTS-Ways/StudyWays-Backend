from django.urls import path
from file.views import Search, MoreUsedFile, AddPhotoUrl, Library1, Library2

urlpatterns = [
    path("search", Search.as_view(), name="search"),
    path("library1", Library1.as_view(), name="library1"),
    path("library2", Library2.as_view(), name="library2"),
    path("more-used", MoreUsedFile.as_view(), name="more-used"),
    path("add-photo-url", AddPhotoUrl.as_view(), name="add-photo-url"),
]
