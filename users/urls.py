from django.urls import path, include
from .views import GoogleLogin, GitHubLogin

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("register/", include("dj_rest_auth.registration.urls")),
    path("social/", include([
        path("google/", GoogleLogin.as_view(), name="google_login"),
        path("github/", GitHubLogin.as_view(), name="github_login"),
    ])),
]
