from django.urls import path
from service.views import Services, ServicesItem, ServicesCorrection, FeedbackView, ServicesCorrectionAI, ServicesCorrectionV2, DraftServices, DraftServicesItem, ServicesCorrectionV3
from service.history import StudentHistory
from .share import ReportShareLink


urlpatterns = [
    path("services", Services.as_view(), name="services"),
    path("service-item/<int:id>/",ServicesItem.as_view(),name="service-item"),
    path("service-correction/<int:id>/",ServicesCorrection.as_view(),name="service-correction"),
    path("service-correction-v2/<int:id>/",ServicesCorrectionV2.as_view(),name="service-correction-v2"),
    path("service-correction-v3/<int:id>/",ServicesCorrectionV3.as_view(),name="service-correction-v3"),
    path("service-correction-ai/<int:id>/",ServicesCorrectionAI.as_view(),name="service-correction-ai"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
    # 
    path("draft-services", DraftServices.as_view(), name="draft-services"),
    path("draft-service-item/<int:id>",DraftServicesItem.as_view(),name="draft-service-item"),
    # 
    path("student-history", StudentHistory.as_view(), name="student-history"),
    # 
    path("share-link", ReportShareLink.as_view(), name="report-link"),
    path("share-link/<str:link>", ReportShareLink.as_view(), name="report-share"),
]
