# Generated by Django 4.1.11 on 2024-04-18 00:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_delete_userdata"),
    ]

    operations = [
        migrations.AddField(
            model_name="chathistory",
            name="title",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
