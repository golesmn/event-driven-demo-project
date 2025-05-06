from django.db import models



class Notification(models.Model):
    title = models.CharField()
    type = models.CharField(choices=(
        ("sms", "SMS"),("push", "PUSH")), null=True, blank=True)

    class Meta:
        db_table = "notifications"
