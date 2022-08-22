from django.db import models

# Create your models here.

class SelfRole(models.Model):
    title = models.CharField(verbose_name="title", max_length=100, null=True)
    server = models.BigIntegerField(verbose_name="server id")
    message_id = models.BigIntegerField(verbose_name="message_id", unique=True)
    reaction = models.CharField(verbose_name="reaction", max_length=1000)
    max_role = models.IntegerField(verbose_name="max_role")
    channel_id = models.BigIntegerField(null=True)
    create_date = models.DateTimeField(verbose_name="create_date",
                                       auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now=True)
    update_by = models.BigIntegerField(null=True)
    created_by = models.CharField(null=True, max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    def who_updated(self):
        if self.update_by is not None:
            return '<@' + str(self.update_by) + '>'