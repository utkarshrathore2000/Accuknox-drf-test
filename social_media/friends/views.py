from django.contrib.auth import get_user_model
from django.db.models import Case, F, IntegerField, Q, Subquery, Value, When
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .filters import UserFilterSet
from .models import Friends
from .serializers import UserListSerializer

User = get_user_model()


class GetUserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    pagination_class = PageNumberPagination

    __doc__ = """
        This api is used to return the list of user also we can search the user via first_name and email
        query_param:
            query:CharField
    """

    def get(self, request, *args, **kwargs):
        user_qs = UserFilterSet(
            request.GET,
            queryset=User.objects.all().order_by("-id"),
        )
        page = self.paginate_queryset(user_qs.qs)
        if page is not None:
            serializer = UserListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserListSerializer(user_qs.qs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class GetFriendListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    pagination_class = PageNumberPagination
    __doc__ = """
            This API view is used to get the list of accepted friends for the authenticated user.
    """

    def get(self, request, *args, **kwargs):
        user_qs = self.get_user_queryset(request.user)
        page = self.paginate_queryset(user_qs)
        serializer = (
            UserListSerializer(page, many=True)
            if page
            else UserListSerializer(user_qs, many=True)
        )
        return (
            self.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data, status=HTTP_200_OK)
        )

    def get_user_queryset(self, user):
        """
        Helper method to get the queryset of accepted friends for the given user.
        """
        return User.objects.filter(id__in=self.get_friend_subquery(user))

    def get_friend_subquery(self, user):
        """
        Helper method to get the subquery for accepted friends based on the given user.
        """
        return (
            Friends.objects.filter(Q(sender=user) | Q(receiver=user), status="accepted")
            .annotate(
                related_user_id=Case(
                    When(sender=user, then=F("receiver__id")),
                    When(receiver=user, then=F("sender__id")),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .values("related_user_id")
        )


class GetFriendRequestListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    pagination_class = PageNumberPagination
    __doc__ = """
            This API view is used to get the list of pending friend requests for the authenticated user.
    """

    def get(self, request, *args, **kwargs):
        user_qs = self.get_user_queryset(request.user)
        page = self.paginate_queryset(user_qs)
        serializer = (
            UserListSerializer(page, many=True)
            if page
            else UserListSerializer(user_qs, many=True)
        )
        return (
            self.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data, status=HTTP_200_OK)
        )

    def get_user_queryset(self, user):
        """
        Helper method to get the queryset of users who sent pending friend requests to the given user.
        """
        return User.objects.filter(id__in=self.get_friend_request_subquery(user))

    def get_friend_request_subquery(self, user):
        """
        Helper method to get the subquery for pending friend requests based on the given user.
        """
        return Friends.objects.filter(receiver=user, status="pending").values(
            "sender__id"
        )
