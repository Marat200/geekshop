# Generated by Django 3.2.8 on 2021-11-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
