# Generated by Django 2.1.7 on 2020-07-25 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20200725_1547'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AreaOfInterest',
        ),
        migrations.DeleteModel(
            name='CourtPreference',
        ),
    ]