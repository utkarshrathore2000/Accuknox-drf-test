from django.urls import path

from .views import GetUserListView


urlpatterns = [
    path("get-user-list/", GetUserListView.as_view(), name='get-user-list'),

]