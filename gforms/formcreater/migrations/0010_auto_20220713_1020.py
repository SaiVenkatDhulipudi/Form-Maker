# Generated by Django 3.2.13 on 2022-07-13 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formcreater', '0009_auto_20220713_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='formresponses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.JSONField()),
                ('qid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formcreater.question')),
            ],
        ),
        migrations.CreateModel(
            name='response',
            fields=[
                ('responseid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('formid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formcreater.forms')),
            ],
        ),
        migrations.DeleteModel(
            name='responses',
        ),
        migrations.AddField(
            model_name='formresponses',
            name='responseid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formcreater.response'),
        ),
    ]
