# Generated by Django 3.0.2 on 2020-01-18 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_auto_20200118_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='series_type',
            field=models.CharField(default='close', max_length=10),
        ),
    ]