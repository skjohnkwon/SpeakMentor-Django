# Generated by Django 4.1.11 on 2024-04-29 07:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_rename_age_questionnaire_birth_year"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="practicelist",
            name="user",
        ),
        migrations.DeleteModel(
            name="PracticeHistory",
        ),
        migrations.DeleteModel(
            name="PracticeList",
        ),
    ]
