# Generated by Django 2.1.7 on 2020-03-13 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('law', '0003_lawinnercategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawcategory',
            name='indictable_offence',
            field=models.BooleanField(default=False, verbose_name='Indictable Offence'),
        ),
        migrations.AddField(
            model_name='lawcategory',
            name='summary_offence',
            field=models.BooleanField(default=False, verbose_name='Summary Offence'),
        ),
    ]
