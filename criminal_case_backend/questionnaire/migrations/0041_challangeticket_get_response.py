# Generated by Django 2.1.7 on 2021-01-24 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0040_auto_20210123_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='challangeticket',
            name='get_response',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
