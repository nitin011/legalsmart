# Generated by Django 2.1.7 on 2020-09-02 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0035_auto_20200830_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='is_age_confirm',
            field=models.CharField(default='', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='userresponse',
            name='is_authorise',
            field=models.CharField(default='', max_length=120, null=True),
        ),
    ]