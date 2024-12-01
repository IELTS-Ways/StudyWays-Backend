from django.urls import path
from service.views import Services, ServicesItem, ServicesCorrection, FeedbackView, ServicesCorrectionAI
from service.history import StudentHistory
from .share import ReportShareLink

urlpatterns = [
    path("services", Services.as_view(), name="services"),
    path("service-item/<int:id>/",ServicesItem.as_view(),name="service-item"),
    path("service-correction/<int:id>/",ServicesCorrection.as_view(),name="service-correction"),
    path("service-correction-ai/<int:id>/",ServicesCorrectionAI.as_view(),name="service-correction-ai"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
    # 
    path("student-history", StudentHistory.as_view(), name="student-history"),
    # 
    path("share-link", ReportShareLink.as_view(), name="report-link"),
    path("share-link/<str:link>", ReportShareLink.as_view(), name="report-share"),
]
