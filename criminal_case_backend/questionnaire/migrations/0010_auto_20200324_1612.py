# Generated by Django 2.1.7 on 2020-03-24 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0009_auto_20200318_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='is_dropdown',
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='option_type',
            field=models.CharField(choices=[('1', 'radio'), ('2', 'dropdown'), ('3', 'spinner'), ('4', 'text')], default=1, help_text='Option Types', max_length=50),
            preserve_default=False,
        ),
    ]
