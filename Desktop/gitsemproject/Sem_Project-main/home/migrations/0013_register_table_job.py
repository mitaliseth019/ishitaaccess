# Generated by Django 3.1.7 on 2021-05-11 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20210501_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_table',
            name='job',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
