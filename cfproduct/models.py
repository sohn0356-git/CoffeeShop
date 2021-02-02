from django.db import models
from cfuser.models import Cfuser


BUY_CHOICES = (
    (0, 'credit'),
    (1, 'cash'),
    (2, 'kakaopay')
)

# Create your models here.
# Create your models here.
class Cfproduct(models.Model):
    name = models.CharField(max_length=50,verbose_name='이름')
    price = models.IntegerField(verbose_name='price')
    image = models.ImageField(blank=True, null=True)
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

class BuyInfo(models.Model):
    buyer = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE,verbose_name='구매자')
    address = models.CharField(max_length=50,verbose_name='주소')
    buy_method = models.SmallIntegerField(choices=BUY_CHOICES)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'buyer info'
        verbose_name = '구매정보'
        verbose_name_plural = '구매정보'

class Buy(models.Model):
    buy_info = models.ForeignKey('cfproduct.BuyInfo', on_delete=models.CASCADE,verbose_name='구매정보')
    cfname = models.ForeignKey('cfproduct.Cfproduct', on_delete=models.CASCADE,verbose_name='커피')
    quantity = models.IntegerField(default=0, verbose_name='주문수량')

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'buy detail'
        verbose_name = '구매'
        verbose_name_plural = '구매'
