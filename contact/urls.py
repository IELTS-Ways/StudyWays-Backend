from django.urls import path
from .views import ContactUsView,ApplicationFormView

urlpatterns = [
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('application/', ApplicationFormView.as_view(), name='application'),
]
