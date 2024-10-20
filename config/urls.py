from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from config.settings import STATIC_ROOT, STATIC_URL, MEDIA_URL, MEDIA_ROOT
from . import views
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework import serializers


schema_view = get_schema_view(
    openapi.Info(
        title="StudyWays API",
        default_version='v1',
        description="API documentation for StudyWays",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)



urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', views.index, name='home'),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("files/", include("file.urls")),
    path("blog/", include("blog.urls")),
    path("subscription/", include("subscription.urls")),
    path("service/", include("service.urls")),
    path("auth/", include('drf_social_oauth2.urls', namespace="drf")),
    path("google-signup/", views.GoogleAuthRedirect.as_view()),
    path("google-redirect/", views.GoogleRedirectURIView.as_view()),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
