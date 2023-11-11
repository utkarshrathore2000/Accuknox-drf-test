from django.urls import path

from .views import GetFriendListView, GetFriendRequestListView, GetUserListView

urlpatterns = [
    path("get-user-list/", GetUserListView.as_view(), name="get-user-list"),
    path("get-friend-list/", GetFriendListView.as_view(), name="get-friend-list"),
    path(
        "get-friend-request-list/",
        GetFriendRequestListView.as_view(),
        name="get-friend-request-list",
    ),
]
