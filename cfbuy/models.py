from django.db import models

from cfuser.models import Cfuser
from cfproduct.models import Cfproduct
# Create your models here.

BUY_CHOICES = (
    (0, 'credit'),
    (1, 'cash'),
    (2, 'kakaopay')
)

class Buy(models.Model):
    buyer = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE,verbose_name='구매자')
    address = models.CharField(max_length=50,verbose_name='주소')
    buy_method = models.SmallIntegerField(choices=BUY_CHOICES)
    buy_date = models.DateTimeField(auto_now_add=True, verbose_name='구매일자')

    def __str__(self):
        return "Buy Info No."+str(self.id)+" "+self.buyer.name
    
    class Meta:
        db_table = 'buyer info'
        verbose_name = '구매'
        verbose_name_plural = '구매'

class Buydetail(models.Model):
    buy_info = models.ForeignKey('cfbuy.Buy', on_delete=models.CASCADE,verbose_name='구매정보')
    amount = models.IntegerField(default=0, verbose_name='주문 총 금액')

    def __str__(self):
        return "Buy Detail No."+str(self.buy_info.id)+"_"+str(self.id)
    
    class Meta:
        db_table = 'buyer detail'
        verbose_name = '구매상세'
        verbose_name_plural = '구매상세'

class Shoppingbasket(models.Model):
    buyer = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE,verbose_name='구매자')

    def __str__(self):
        return "Basket Info No."+str(self.id)+" "+self.buyer.name
    
    class Meta:
        db_table = 'basket table'
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니'

class Basketdetail(models.Model):
    basket = models.ForeignKey('cfbuy.Shoppingbasket', on_delete=models.CASCADE,verbose_name='장바구니')
    amount = models.IntegerField(default=0, verbose_name='금액')

    def __str__(self):
        return "Basket Detail No."+str(self.basket.id)+"_"+str(self.id)
    
    class Meta:
        db_table = 'basket detail'
        verbose_name = '장바구니상세'
        verbose_name_plural = '장바구니상세'

class Cfselect(models.Model):
    cfoption = models.ForeignKey('cfproduct.CftoOption', on_delete=models.CASCADE,verbose_name='구매제품')
    buy = models.ForeignKey('cfbuy.Buydetail', on_delete=models.CASCADE,verbose_name='구매내역', blank=True, null=True)
    basket = models.ForeignKey('cfbuy.Basketdetail', on_delete=models.CASCADE,verbose_name='장바구니내역', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'coffee select'
        verbose_name = '구매제품'
        verbose_name_plural = '구매제품'