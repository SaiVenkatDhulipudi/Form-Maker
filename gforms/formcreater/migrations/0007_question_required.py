# Generated by Django 3.2.13 on 2022-07-12 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formcreater', '0006_responses'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.CharField(default='', max_length=20),
        ),
    ]