# Generated by Django 4.2.1 on 2023-07-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='remaining_free_minutes',
            field=models.FloatField(default=12.0),
        ),
    ]
