# Generated by Django 2.1.7 on 2020-06-05 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_locations_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='os_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
