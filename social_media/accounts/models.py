from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    """A user in the system. Users in this system can all theoretically upload or edit essays. Everyone has the
    same level of access, for the sake of simplicity. Users need to be authenticated to do anything in the system
    other than login.

    This class is defined according to Django recommendations to allow additional fields to be added to our
    User class. Reference settings.
    """
    email = models.EmailField(_('email address') , unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"user:- {self.pk}"