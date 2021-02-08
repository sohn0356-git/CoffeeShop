# Generated by Django 3.1.5 on 2021-02-08 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cfuser', '0001_initial'),
        ('cfbuy', '0003_basketdetail_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketdetail',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cfuser.cfuser', verbose_name='구매자'),
        ),
    ]
