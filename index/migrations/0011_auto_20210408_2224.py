# Generated by Django 3.1.7 on 2021-04-08 14:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20210408_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='leasehistory',
            name='leasePropertyID',
            field=models.IntegerField(default=1, help_text='財產ID', verbose_name='財產ID'),
        ),
        migrations.AlterField(
            model_name='leasehistory',
            name='agree_date',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now, verbose_name='同意日期'),
        ),
        migrations.AlterField(
            model_name='leasehistory',
            name='borrow_date',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now, verbose_name='借用日期'),
        ),
        migrations.AlterField(
            model_name='leasehistory',
            name='return_date',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now, verbose_name='歸還日期'),
        ),
    ]
