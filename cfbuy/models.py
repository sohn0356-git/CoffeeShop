from django.db import models
from django.utils.timezone import now
from cfuser.models import Cfuser
from cfproduct.models import Cfproduct, Coffeecode
# Create your models here.

BUY_CHOICES = (
    (0, 'credit'),
    (1, 'cash'),
    (2, 'kakaopay')
)

class Cfbuy(models.Model):
    buyer = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE,verbose_name='구매자')
    recipient = models.CharField(max_length=20, verbose_name='수령인', default='')
    postcode = models.CharField(max_length=20,verbose_name='우편번호', default='')
    address = models.CharField(max_length=50,verbose_name='주소', default='')
    extraAddress = models.CharField(max_length=50,verbose_name='참고항목',blank='true', null='true')
    detailAddress = models.CharField(max_length=50,verbose_name='상세주소', default='')
    buy_method = models.SmallIntegerField(choices=BUY_CHOICES)
    phone = models.CharField(max_length=20, verbose_name='전화번호', default='')
    phone1 = models.CharField(max_length=20, verbose_name='전화번호1', default='')
    phone2 = models.CharField(max_length=20, verbose_name='전화번호2', default='')
    phone3 = models.CharField(max_length=20, verbose_name='전화번호3', default='')
    email = models.CharField(max_length=50, verbose_name='email', default='')
    email_name = models.CharField(max_length=20, verbose_name='이메일이름', default='')
    email_domain = models.CharField(max_length=20, verbose_name='이메일도메인', default='')
    delivery_msg = models.CharField(max_length=100, verbose_name='delivery_msg', default='',blank='true', null='true')
    buy_date = models.DateTimeField(default=now, verbose_name='구매일자')

    def __str__(self):
        return "Buy Info No."+str(self.id)+" "+self.buyer.name
    
    class Meta:
        db_table = 'buyer info'
        verbose_name = '구매'
        verbose_name_plural = '구매'

class Buydetail(models.Model):
    buy_info = models.ForeignKey('cfbuy.Cfbuy', on_delete=models.CASCADE,verbose_name='구매정보')
    amount = models.IntegerField(default=0, verbose_name='주문 총 금액')
    quantity = models.IntegerField(verbose_name='수량', default=1)

    def __str__(self):
        return "Buy Detail No."+str(self.buy_info.id)+"_"+str(self.id)
    
    class Meta:
        db_table = 'buyer detail'
        verbose_name = '구매상세'
        verbose_name_plural = '구매상세'

class Basketdetail(models.Model):
    buyer = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE,verbose_name='구매자')
    amount = models.IntegerField(default=0, verbose_name='금액')
    total = models.IntegerField(default=0, verbose_name='총금액')
    quantity = models.IntegerField(verbose_name='수량', default=1)

    def __str__(self):
        return "Basket Detail No."+"_"+str(self.id)
    
    class Meta:
        db_table = 'basket detail'
        verbose_name = '장바구니상세'
        verbose_name_plural = '장바구니상세'

class Cfselect(models.Model):
    cfoption = models.ForeignKey('cfproduct.CftoOption', on_delete=models.CASCADE,verbose_name='구매제품')
    buy = models.ForeignKey('cfbuy.Buydetail', on_delete=models.CASCADE,verbose_name='구매내역', blank=True, null=True)
    basket = models.ForeignKey('cfbuy.Basketdetail', on_delete=models.CASCADE,verbose_name='장바구니내역', blank=True, null=True)
    cf_code = models.ForeignKey('cfproduct.Coffeecode', on_delete=models.CASCADE,verbose_name='커피코드', null=True)
    buy_date = models.DateTimeField(default=now, verbose_name='구매일자')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'coffee select'
        verbose_name = '구매제품'
        verbose_name_plural = '구매제품'