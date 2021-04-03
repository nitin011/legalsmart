# Generated by Django 2.1.7 on 2020-06-08 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_fcm_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fcm_token',
        ),
        migrations.AlterField(
            model_name='roles',
            name='role',
            field=models.CharField(choices=[('attorney', 'attorney'), ('juror', 'juror'), ('user', 'user'), ('judge', 'judge')], help_text='Designates whether the user', max_length=120),
        ),
    ]