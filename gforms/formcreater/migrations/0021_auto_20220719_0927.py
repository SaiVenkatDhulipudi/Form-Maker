# Generated by Django 3.2.13 on 2022-07-19 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic=False
    dependencies = [
        ('formcreater', '0020_alter_choice_choices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='response',
            old_name='responseid',
            new_name='response_id',
        ),
        migrations.AlterField(
            model_name='formresponses',
            name='response_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='formcreater.response'),
        ),
        migrations.AlterField(
            model_name='response',
            name='form_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_responses', to='formcreater.forms'),
        ),
    ]