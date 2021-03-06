# Generated by Django 3.1.5 on 2021-01-26 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cfuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='제목')),
                ('contents', models.TextField(verbose_name='내용')),
                ('hits', models.IntegerField(default=0, verbose_name='조회수')),
                ('disclosure', models.SmallIntegerField(choices=[(0, 'private'), (1, 'public')])),
                ('registered_dttm', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cfuser.cfuser', verbose_name='작성자')),
            ],
            options={
                'verbose_name': 'cfboard',
                'verbose_name_plural': 'cfboards',
                'db_table': 'coffeeshop board',
            },
        ),
    ]
