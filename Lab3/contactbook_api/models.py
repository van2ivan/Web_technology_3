from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    is_online = models.BooleanField(default=False)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"))


# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    contact_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.IntegerField(unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        contact = {"name": self.contact_name, "number": self.phone_number}
        return contact
