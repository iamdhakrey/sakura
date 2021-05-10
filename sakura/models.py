from django.db import models

# Create your models here.

class ImagesModel(models.Model):
    image1  = models.ImageField(verbose_name="image1",upload_to='welcome_images/',width_field=1920,height_field=872)
    image2  = models.ImageField(verbose_name="image2",upload_to='welcome_images/',width_field=1920,height_field=872)
    image3  = models.ImageField(verbose_name="image3",upload_to='welcome_images/',width_field=1920,height_field=872)

class WelcomeData(models.Model):
    server_id       =  models.BigIntegerField(primary_key=True)
    server_name     =  models.CharField(verbose_name="server_name", max_length=100)
    guild_id        =  models.BigIntegerField()
    server_active   =  models.BooleanField(default=True)
    welcome_enable  =  models.BooleanField(default=False)
    self_role       =  models.BigIntegerField(null=True)
    welcome_channel =  models.BigIntegerField(null=True)
    welcome_images  =  models.ForeignKey(ImagesModel,on_delete=models.CASCADE)
    welcome_msg     =  models.CharField(max_length=3000)
    update_by       =  models.BigIntegerField(null=True)
    last_update     =  models.DateTimeField(null=True)

    def save(self,*args, **kwargs):
        super(WelcomeData,self).save(*args, **kwargs)
