from django.db import models
from cfuser.models import Cfuser
from CoffeeShop.settings import MEDIA_ROOT


# Create your models here.
# Create your models here.
class Cfproduct(models.Model):
    name = models.CharField(max_length=50,verbose_name='이름')
    price = models.IntegerField(verbose_name='price')
    image = models.ImageField(blank=True, null=True, upload_to="images", default='default.jpg')
    cfcode = models.ForeignKey('cfproduct.Coffeecode', on_delete=models.CASCADE,verbose_name='커피종류')
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'coffeeshop coffee'
        verbose_name = '커피'
        verbose_name_plural = '커피'

class Coffeecode(models.Model):
    cfcode = models.CharField(max_length=50)
    
    def __str__(self):
        return self.cfcode
    
    class Meta:
        db_table = 'cfcode name'
        verbose_name = '커피 코드'
        verbose_name_plural = '커피 코드'

