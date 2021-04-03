# Generated by Django 2.1.7 on 2021-01-28 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0043_challangeticket_accept_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='challangeticket',
            name='accepted_by_contact',
            field=models.CharField(default='', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='challangeticket',
            name='accepted_by_name',
            field=models.CharField(default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='challangeticket',
            name='rep_status',
            field=models.BooleanField(default=False),
        ),
    ]
