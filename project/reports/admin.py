from django.contrib import admin

# Register your models here.
from .models import Report
# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_name",
        "case_number",
        "case_result",
        "comment",
        "user_created_login",
        "user_created_name",
        "user_created_email",
        "report_name",
        "update_time",
    )
    ordering = ['-id']


admin.site.register(Report, ReportAdmin)
