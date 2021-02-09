from django.db import models
from cfuser.models import Cfuser
from CoffeeShop.settings import MEDIA_ROOT
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F


# Create your models here.
# Create your models here.
class Coffeecode(models.Model):
    cfcode = models.CharField(max_length=50)
    
    def __str__(self):
        return self.cfcode
    
    class Meta:
        db_table = 'cfcode name'
        verbose_name = '커피 코드'
        verbose_name_plural = '커피 코드'

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

class Opcode(models.Model):
    title = models.CharField(max_length=30, verbose_name='옵션명')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'option title'
        verbose_name = '옵션코드'
        verbose_name_plural = '옵션코드'

class CftoOption(models.Model):
    coffee_id = models.ForeignKey('cfproduct.Cfproduct', on_delete=models.CASCADE,verbose_name='커피명')
    option_id = models.ForeignKey('cfproduct.Cfoption', on_delete=models.CASCADE,verbose_name='옵션')
    amount = models.IntegerField(verbose_name='추가금액', default=0)
    
    def __str__(self):
        return self.coffee_id.name +'(' + self.option_id.code_option.title + ' : ' + self.option_id.option + ')'

    class Meta:
        db_table = 'coffee to option'
        verbose_name = '커피_옵션'
        verbose_name_plural = '커피_옵션'

class Cfoption(models.Model):
    code_option = models.ForeignKey('cfproduct.Opcode', on_delete=models.CASCADE,verbose_name='옵션코드', default='')
    option = models.CharField(max_length=30, verbose_name='옵션', default='')
    

    def __str__(self):
        return self.code_option.title + " : " + self.option

    class Meta:
        db_table = 'coffee option'
        verbose_name = '옵션'
        verbose_name_plural = '옵션'

class Cfcomment(models.Model):
    coffee = models.ForeignKey('cfproduct.Cfproduct', on_delete=models.CASCADE,verbose_name='커피')
    user = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE, verbose_name='작성자')
    contents = models.TextField(verbose_name='내용')
    

    def __str__(self):
        return self.coffee.name + self.user.name
    
    class Meta:
        db_table = 'coffee comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
