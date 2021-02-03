from django.db import models

# Create your models here.

# BUY_CHOICES = (
#     (0, 'credit'),
#     (1, 'cash'),
#     (2, 'kakaopay')
# )

# class BuyInfo(models.Model):
#     buyer = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE,verbose_name='구매자')
#     address = models.CharField(max_length=50,verbose_name='주소')
#     buy_method = models.SmallIntegerField(choices=BUY_CHOICES)
#     buy_date = models.DateTimeField(auto_now_add=True, verbose_name='구매일자')

#     def __str__(self):
#         return str(self.id)
    
#     class Meta:
#         db_table = 'buyer info'
#         verbose_name = '구매정보'
#         verbose_name_plural = '구매정보'

# class Buy(models.Model):
#     buy_info = models.ForeignKey('cfproduct.BuyInfo', on_delete=models.CASCADE,verbose_name='구매정보')
#     cfname = models.ForeignKey('cfproduct.Cfproduct', on_delete=models.CASCADE,verbose_name='커피')
#     quantity = models.IntegerField(default=0, verbose_name='주문수량')
    

#     def __str__(self):
#         return str(self.id)
    
#     class Meta:
#         db_table = 'buy detail'
#         verbose_name = '구매'
#         verbose_name_plural = '구매'

# class Shopping_basket(models.Model):
#     pass