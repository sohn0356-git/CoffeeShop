# Generated by Django 3.1.5 on 2021-02-08 08:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cfbuy', '0011_auto_20210208_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='buydetail',
            name='buy_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='구매일자'),
        ),
    ]