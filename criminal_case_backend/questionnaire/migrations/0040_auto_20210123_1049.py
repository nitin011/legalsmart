# Generated by Django 2.1.7 on 2021-01-23 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0039_auto_20201118_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='challangeticket',
            name='challange_ticket',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='challangeticket',
            name='deadline_comingup',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='challangeticket',
            name='name',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
