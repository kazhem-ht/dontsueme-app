from django.db import models

# Create your models here.


class Report(models.Model):

    JUSTICE_CHOICES = (("not_guilty", "Не виновен"), ("guilty", "Виновен"))

    client_name = models.CharField(
        max_length=255,
        verbose_name="ФИО клиента")

    case_number = models.IntegerField(verbose_name="Номер дела")

    case_result = models.CharField(
        verbose_name="Приговор",
        choices=JUSTICE_CHOICES,
        max_length=12,
        default="not_guilty"
    )
    comment = models.TextField(
        max_length=255,
        verbose_name="Комментарий",
        default='',
        blank=True)

    user_created_login = models.CharField(
        max_length=255,
        verbose_name="Логин юриста")

    user_created_name = models.CharField(
        max_length=255,
        verbose_name="Имя юриста",
        blank=True, default='')

    user_created_email = models.CharField(
        max_length=255,
        verbose_name="Email юриста",
        blank=True, default='')

    report_html = models.TextField(
        max_length=255,
        verbose_name="Отчет HTML",
        default='',
        blank=True)

    report_name = models.CharField(
        max_length=255,
        verbose_name="Имя отчета",
        blank=True,
        default='')


    update_time = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Time of last update")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
