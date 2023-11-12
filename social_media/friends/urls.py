from django.urls import path

from .views import (AcceptRejectFriendRequestView, GetFriendListView,
                    GetFriendRequestListView, GetUserListView,
                    SendFriendRequestView)

urlpatterns = [
    path("get-user-list/", GetUserListView.as_view(), name="get-user-list"),
    path("get-friend-list/", GetFriendListView.as_view(), name="get-friend-list"),
    path(
        "get-friend-request-list/",
        GetFriendRequestListView.as_view(),
        name="get-friend-request-list",
    ),
    path(
        "send-friend-request/",
        SendFriendRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "accept-friend-request/<int:friend_id>/",
        AcceptRejectFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "reject-friend-request/<int:friend_id>/",
        AcceptRejectFriendRequestView.as_view(),
        name="reject-friend-request",
    ),
]
