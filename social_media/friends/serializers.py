from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Friends

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "date_joined", "is_active"]


class FriendSerializer(serializers.ModelSerializer):
    receiver_user = UserListSerializer(source="receiver")
    sender_user = UserListSerializer(source="sender")

    class Meta:
        model = Friends
        fields = ["id", "receiver", "sender_user", "receiver_user", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receiver"].required = True
        for field_name in self.fields.keys():
            if field_name != "receiver":
                self.fields[field_name].required = False
