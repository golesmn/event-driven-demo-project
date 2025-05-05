from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    username = models.CharField()
    hashed_password = models.CharField()
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"
