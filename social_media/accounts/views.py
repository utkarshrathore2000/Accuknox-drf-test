from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import SignUpSerializer
from .utils import get_user_token


class SignUpApiView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    __doc__ = """
                SignUp Api view this api is used to create the user
                params:
                   email: EmailField
                   password: CharField
                   first_name: CharField
                   last_name: CharField
            """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = get_user_token(request)
            response_status = status.HTTP_201_CREATED
        else:
            response_data = {"message": "Unable to create user"}
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response_data, status=response_status)
