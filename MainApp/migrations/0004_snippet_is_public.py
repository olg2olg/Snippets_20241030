# Generated by Django 5.1.2 on 2024-10-31 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_snippet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
