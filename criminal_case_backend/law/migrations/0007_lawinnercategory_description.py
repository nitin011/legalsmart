# Generated by Django 2.2 on 2020-03-18 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('law', '0006_auto_20200313_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawinnercategory',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
