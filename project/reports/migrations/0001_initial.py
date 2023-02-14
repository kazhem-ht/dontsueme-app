# Generated by Django 4.1.5 on 2023-02-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Report",
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
                    "client_name",
                    models.CharField(max_length=255, verbose_name="ФИО клиента"),
                ),
                ("case_number", models.IntegerField(verbose_name="Номер дела")),
                (
                    "case_result",
                    models.CharField(
                        choices=[("not_guilty", "Не виновен"), ("guilty", "Виновен")],
                        default="not_guilty",
                        max_length=12,
                        verbose_name="Приговор",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Комментарий",
                    ),
                ),
                (
                    "user_created_login",
                    models.CharField(max_length=255, verbose_name="Логин юриста"),
                ),
                (
                    "user_created_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Имя юриста",
                    ),
                ),
                (
                    "report_html",
                    models.TextField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Отчет HTML",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Time of last update"
                    ),
                ),
            ],
            options={
                "verbose_name": "Report",
                "verbose_name_plural": "Reports",
            },
        ),
    ]
