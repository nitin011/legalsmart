# Generated by Django 2.1.7 on 2020-03-28 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0014_auto_20200328_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='law_inner_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='law.LawInnerCategory'),
        ),
    ]