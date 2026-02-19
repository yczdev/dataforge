from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchemaViewSet, schema_download_view, CreateUserView, CustomAuthToken

router = DefaultRouter()
router.register(r"schemas", SchemaViewSet, basename="schema")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", CustomAuthToken.as_view(), name="login"),

    path("schemas/<int:pk>/download/", schema_download_view, name="schema-download"),
    path("", include(router.urls)),
]