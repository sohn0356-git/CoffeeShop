# Generated by Django 3.1.5 on 2021-02-08 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfbuy', '0006_auto_20210208_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfbuy',
            name='email_domain',
            field=models.CharField(default='', max_length=20, verbose_name='이메일도메인'),
        ),
        migrations.AddField(
            model_name='cfbuy',
            name='email_name',
            field=models.CharField(default='', max_length=20, verbose_name='이메일이름'),
        ),
        migrations.AddField(
            model_name='cfbuy',
            name='phone1',
            field=models.CharField(default='', max_length=20, verbose_name='전화번호1'),
        ),
        migrations.AddField(
            model_name='cfbuy',
            name='phone2',
            field=models.CharField(default='', max_length=20, verbose_name='전화번호2'),
        ),
        migrations.AddField(
            model_name='cfbuy',
            name='phone3',
            field=models.CharField(default='', max_length=20, verbose_name='전화번호3'),
        ),
    ]
