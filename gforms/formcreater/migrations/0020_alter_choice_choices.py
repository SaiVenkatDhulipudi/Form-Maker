# Generated by Django 3.2.13 on 2022-07-19 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formcreater', '0019_auto_20220719_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choices',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
