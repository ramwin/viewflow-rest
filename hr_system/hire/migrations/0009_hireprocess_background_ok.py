# Generated by Django 3.1.3 on 2020-11-07 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0008_auto_20201107_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='hireprocess',
            name='background_ok',
            field=models.BooleanField(blank=True, null=True, verbose_name='背景调查是否通过'),
        ),
    ]
