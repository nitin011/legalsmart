# Generated by Django 2.1.7 on 2020-03-08 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200308_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
