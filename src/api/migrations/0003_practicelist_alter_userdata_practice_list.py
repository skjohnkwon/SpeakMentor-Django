# Generated by Django 4.1.11 on 2024-04-15 20:27

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0002_chathistory_alter_userdata_chat_history"),
    ]

    operations = [
        migrations.CreateModel(
            name="PracticeList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "words",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=100),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        # migrations.AlterField(
        #     model_name="userdata",
        #     name="practice_list",
        #     field=models.ForeignKey(
        #         blank=True,
        #         null=True,
        #         on_delete=django.db.models.deletion.CASCADE,
        #         to="api.practicelist",
        #     ),
        # ),
        migrations.RemoveField(
            model_name="userdata",
            name="practice_list",
        ),
        migrations.AddField(
            model_name="userdata",
            name="practice_list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.practicelist",
            ),
        ),
    ]
