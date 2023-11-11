from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .filters import UserFilterSet
from .serializers import UserListSerializer

from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination


User = get_user_model()


class GetUserListView(ListAPIView):
    serializer_class = UserListSerializer
    pagination_class = PageNumberPagination
    __doc__ = """
        This api is used to return the list of user also we can search the user via first_name and email
        query_param:
            query:CharField
    """

    def get(self , request , *args , **kwargs):
        user_qs = UserFilterSet(
            request.GET,
            queryset=User.objects.all().order_by("-id") ,
        )
        page = self.paginate_queryset(user_qs.qs)
        if page is not None:
            serializer = UserListSerializer(page , many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserListSerializer(user_qs.qs , many=True)
        return Response(serializer.data , status=HTTP_200_OK)
