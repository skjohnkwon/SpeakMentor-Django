# Generated by Django 4.1.11 on 2024-04-24 01:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_practicelist_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="practicelist",
            name="modified_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
