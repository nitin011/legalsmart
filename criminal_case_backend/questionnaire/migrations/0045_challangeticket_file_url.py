# Generated by Django 2.1.7 on 2021-02-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0044_auto_20210128_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='challangeticket',
            name='file_url',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
