from typing import Optional
import boto3
from botocore.config import Config

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView, View
from django.views.generic import FormView
from reports.forms import ReportForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from .models import Report
import requests
import logging

class CreateReportView(LoginRequiredMixin, FormView):
    template_name = "reports/create_report.html"
    form_class = ReportForm

    @staticmethod
    def put_report_to_s3(db_report: Report, s3_key: dict) -> str:

        s3_config = Config(region_name=settings.S3_REGION)
        s3_session = boto3.session.Session(
            aws_access_key_id=s3_key['access_key'],
            aws_secret_access_key=s3_key['secret_key'])
        s3 = s3_session.client(
            service_name='s3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            config=s3_config
        )

        object_name = f"{settings.S3_BUCKET_FOLDER}/{db_report.user_created_login}/{db_report.report_name}"
        s3.put_object(Bucket=settings.S3_BUCKET_NAME, Key=object_name,
                      Body=db_report.report_html, StorageClass='COLD')
        return object_name


    def get_yc_lockbox_secret(self, iam_token: str) -> Optional[dict]:
        secret_id = settings.YC_LOCKBOX_SECRET_ID
        secret_data = None
        if settings.S3_KEY:
            secret_data = {"access_key": settings.S3_KEY.split(":")[0],
                           "secret_key": settings.S3_KEY.split(":")[1]}
            return secret_data
        if secret_id:
            get_secret_url = f"https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/{secret_id}/payload"
            headers = {"Authorization": f"Bearer {iam_token}"}
            try:
                response = requests.get(get_secret_url,
                                        headers=headers,
                                        timeout=2)
                if 200 <= response.status_code < 300:
                    response_data = response.json()
                    s3_static_key = {}
                    for entry in response_data['entries']:
                        if entry['key'] == 'access_key':
                           s3_static_key['access_key'] = entry['textValue']
                        elif entry['key'] == 'secret_key':
                           s3_static_key['secret_key'] = entry['textValue']
                    if len(s3_static_key) == 2:
                        logging.info(
                            f"Storage S3 static key recieved from Lockbox id {secret_id}.")
                        return s3_static_key
                    else:
                        logging.error(
                            f"Length of s3_static_key is not 2. Lockbox id {secret_id}")
                        messages.add_message(
                            self.request, messages.ERROR,
                            f'Ошибка получение IAM токена из сервиса метаданных: проверьте логи')
                else:
                    logging.error("Metadata response failed: %s: %s",
                                  response.status_code, response.text)
                    messages.add_message(
                        self.request, messages.ERROR,
                        f'Ошибка получение IAM токена из сервиса Yandex Lockbox id {secret_id}: {response.status_code}, {response.text}')

            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
                logging.error(e)
                messages.add_message(self.request, messages.ERROR, e)
        return secret_data


    def get_yc_iam_token(self) -> Optional[str]:
        iam_token = settings.YC_IAM_TOKEN
        if not iam_token:
            logging.info("Requesting metadata %s for iam token",
                         settings.YC_IAM_TOKEN_METADATA_URL)
            try:
                response = requests.get(settings.YC_IAM_TOKEN_METADATA_URL,
                                        headers={"Metadata-Flavor": "Google"},
                                        timeout=2)
                if 200 <= response.status_code < 300:
                    response_data = response.json()
                    iam_token = response_data["access_token"]

                    logging.info("IAM token recieved from metadata. Expires in  %s",
                                 iam_token['expires_in'])
                else:
                    logging.error("Metadata response failed: %s: %s",
                                response.status_code, response.text)
                    messages.add_message(
                        self.request, messages.ERROR,
                        f'Ошибка получение cтатического ключа из LockBox: {response.status_code}, {response.text}')
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
                logging.error(e)
                messages.add_message(self.request, messages.ERROR, e)
        else:
            logging.info("IAM token recieved from ENV")

        return iam_token

    def create_db_report(self, form_data):
        db_report = Report.objects.create(
            client_name=form_data['client'],
            case_number=form_data['case_number'],
            case_result=form_data['case_result'],
            comment=form_data['comment'],
            user_created_login=self.request.user.username,
            user_created_name=f"{self.request.user.first_name} {self.request.user.last_name}",
            user_created_email=self.request.user.email,
        )
        report_name = f"{db_report.user_created_login}_{db_report.id:03}_{db_report.case_number:05}.html"
        html_report = render_to_string(
            "reports/report.html", {"report_db": db_report})
        db_report.report_name = report_name
        db_report.report_html = html_report
        db_report.save()
        return db_report

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form_data = form.clean()

        iam_token = self.get_yc_iam_token()
        if not iam_token and not settings.S3_KEY:
            messages.add_message(self.request, messages.ERROR,
                                 f'Отчет не сформирован - отсутсвует IAM токен для доступа в Yandex Lockbox')
            return super().form_valid(form)

        s3_keys = self.get_yc_lockbox_secret(iam_token)
        if not s3_keys:
            messages.add_message(self.request, messages.ERROR,
                                 f'Отчет не сформирован - отсутсвует S3 ключ для доступа в Yandex Object Storage')
            return super().form_valid(form)

        db_report = self.create_db_report(form_data)
        get_report_url = reverse('reports:get', kwargs={
                                 'report_id': db_report.id})
        report_link = f'<a target = "_blank" rel = "noopener noreferrer" href = "{get_report_url}">{db_report.report_name}</a>'
        report_link = mark_safe(report_link)

        s3_object_name = self.put_report_to_s3(db_report, s3_keys)
        messages.add_message(self.request, messages.SUCCESS,
                             f'Отчет {report_link} успешно сохранен в '
                             f'S3 бакет <b>{settings.S3_BUCKET_NAME}</b> по пути <b>{s3_object_name}</b>')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class GetReportView(View):
    def get(self, request, report_id):
        html_reports = Report.objects.filter(id=report_id)
        if html_reports:
            return HttpResponse(html_reports[0].report_html)
        else:
            return HttpResponse(f"No report with id {report_id}")
