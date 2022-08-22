from django.db import models

# Create your models here.

class ImagesModel(models.Model):
    image1 = models.ImageField(verbose_name="image1",
                               upload_to='welcome_images/',
                               width_field=1920,
                               height_field=872)
    image2 = models.ImageField(verbose_name="image2",
                               upload_to='welcome_images/',
                               width_field=1920,
                               height_field=872)
    image3 = models.ImageField(verbose_name="image3",
                               upload_to='welcome_images/',
                               width_field=1920,
                               height_field=872)
                               

class WelcomeData(models.Model):

    server_id = models.BigIntegerField(primary_key=True)
    server_name = models.CharField(verbose_name="server_name", max_length=100)

    server_active = models.BooleanField(default=True)
    welcome_enable = models.BooleanField(default=False)
    self_role = models.BigIntegerField(null=True)
    welcome_channel = models.BigIntegerField(null=True)
    welcome_msg = models.CharField(max_length=3000)
    update_by = models.BigIntegerField(null=True)
    last_update = models.DateTimeField(null=True, auto_now=True)

    image1 = models.ImageField(null=True,
                               verbose_name="image1",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image2 = models.ImageField(null=True,
                               verbose_name="image2",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image3 = models.ImageField(null=True,
                               verbose_name="image3",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image4 = models.ImageField(null=True,
                               verbose_name="image4",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image5 = models.ImageField(null=True,
                               verbose_name="image5",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")

    img_width = models.PositiveIntegerField(default=1920)
    img_height = models.PositiveIntegerField(default=872)

    def who_updated(self):
        if self.update_by is not None:
            return '<@' + str(self.update_by) + '>'

    def mention_welcome_channel(self):
        if self.welcome_channel is not None:
            return '<#' + str(self.welcome_channel) + '>'
        else:
            return None

    def save(self, *args, **kwargs):
        super(WelcomeData, self).save(*args, **kwargs)
