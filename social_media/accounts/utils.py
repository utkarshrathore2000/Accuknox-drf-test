from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


def get_user_token(request):
    user = authenticate(
        email=request.data.get("email"), password=request.data.get("password")
    )
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
