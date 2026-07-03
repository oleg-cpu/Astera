from django.urls import path
from django.views.generic import RedirectView

from .views import RegisterView

urlpatterns = [
    path("", RedirectView.as_view(url="register/", permanent=False), name="index_redirect"),

    path("register/", RegisterView.as_view(), name="register"),
]
