# Generated by Django 4.2.1 on 2023-06-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_translationgo_translation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='review',
            field=models.BooleanField(default=False),
        ),
    ]
