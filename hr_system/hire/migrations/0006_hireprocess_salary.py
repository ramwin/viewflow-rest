# Generated by Django 3.1.3 on 2020-11-07 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0005_auto_20201107_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='hireprocess',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='每月薪资'),
        ),
    ]
