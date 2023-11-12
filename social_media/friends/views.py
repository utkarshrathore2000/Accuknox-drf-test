from django.contrib.auth import get_user_model
from django.db.models import Case, F, IntegerField, Q, Value, When
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, get_object_or_404)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN)
from rest_framework.throttling import UserRateThrottle

from .filters import UserFilterSet
from .models import Friends
from .serializers import FriendSerializer, UserListSerializer

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
            queryset=User.objects.exclude(id=request.user.id).order_by("-id"),
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
            self.serializer_class(page, many=True)
            if page
            else self.serializer_class(user_qs, many=True)
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
    serializer_class = FriendSerializer
    pagination_class = PageNumberPagination
    __doc__ = """
            This API view is used to get the list of pending friend requests for the authenticated user.
    """

    def get(self, request, *args, **kwargs):
        friend_qs = Friends.objects.filter(
            receiver=request.user, status="pending"
        ).select_related("sender", "receiver")
        page = self.paginate_queryset(friend_qs)
        serializer = (
            self.serializer_class(page, many=True)
            if page
            else self.serializer_class(friend_qs, many=True)
        )
        return (
            self.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data, status=HTTP_200_OK)
        )


class SendFriendRequestView(CreateAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    __doc__ = """
            This API is used to send the friend request to the other user
            param:
                receiver: receiver user id
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = self.request.user
        serializer.validated_data["sender"] = sender
        # Ensure that the receiver exists and is not the sender
        receiver_id = serializer.validated_data["receiver"]
        if receiver_id == sender.id:
            return Response(
                {"detail": "Cannot send friend request to yourself."},
                status=HTTP_400_BAD_REQUEST,
            )

        # Ensure that there is no existing friend request between the sender and receiver
        existing_request = Friends.objects.filter(
            sender=sender, receiver_id=receiver_id
        ).exists()
        if existing_request:
            return Response(
                {"detail": "Friend request already sent."}, status=HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=HTTP_201_CREATED)


class AcceptRejectFriendRequestView(UpdateModelMixin, GenericAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    __doc__ = """
            This API is used to send the friend request to the other user
            param:
                status: accepted/rejected
    """

    def patch(self, request, *args, **kwargs):
        instance = get_object_or_404(Friends, pk=self.kwargs.get("friend_id"))
        # Check if the user making the request is the receiver
        if instance.receiver != request.user:
            return Response(
                {"detail": "You don't have permission to perform this action."},
                status=HTTP_403_FORBIDDEN,
            )
        status = request.data.get("status", None)
        if status not in ["accepted", "rejected"]:
            return Response(
                {"detail": 'Invalid status. Use "accepted" or "rejected".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.status = status
        instance.save()
        return Response(self.get_serializer(instance).data, status=HTTP_200_OK)
