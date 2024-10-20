from django.urls import path
from service.views import Services, ServicesItem, ServicesCorrection, FeedbackView, ServicesCorrectionAI


urlpatterns = [
    path("services", Services.as_view(), name="services"),
    path("service-item/<int:id>/",ServicesItem.as_view(),name="service-item"),
    path("service-correction/<int:id>/",ServicesCorrection.as_view(),name="service-correction"),
    path("service-correction-ai/<int:id>/",ServicesCorrectionAI.as_view(),name="service-correction-ai"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
]

