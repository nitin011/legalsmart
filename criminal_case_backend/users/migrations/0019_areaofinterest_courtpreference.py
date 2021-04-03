# Generated by Django 2.1.7 on 2020-07-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20200725_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaOfInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Area Of Interest',
                'verbose_name_plural': 'Area Of Interest',
                'db_table': 'area_of_interest',
            },
        ),
        migrations.CreateModel(
            name='CourtPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Court Preference',
                'verbose_name_plural': 'Court Preference',
                'db_table': 'court_preference',
            },
        ),
    ]
