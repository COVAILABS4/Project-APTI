# Generated by Django 4.2.20 on 2025-03-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='domain_type',
            field=models.CharField(default='tech', max_length=10),
        ),
        migrations.AddField(
            model_name='topic',
            name='tech_type',
            field=models.CharField(default='sw', max_length=10),
        ),
    ]
