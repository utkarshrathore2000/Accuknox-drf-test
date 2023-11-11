from django.db import models

from .constants import FRIEND_STATUS


# Create your models here.
class Friends(models.Model):
    """
    Friends:
        - created_at: It contains the time when someone send a friend request
        - sender: It contains the user who send the friend request
        - receiver: It contains the user to whom the friend request has been sent
        - status: It contains the friendship status between both users
    """

    created_at = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(
        "accounts.user", related_name="sender", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        "accounts.user", related_name="receiver", on_delete=models.CASCADE
    )
    status = models.CharField(choices=FRIEND_STATUS, max_length=40, default="pending")
    objects = models.Manager()
