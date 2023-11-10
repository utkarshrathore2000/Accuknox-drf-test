from django.urls import path

from .views import SignUpApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("sign-up/", SignUpApiView.as_view()),

]

# Generate token
token_urls = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += token_urls