from django.urls import path

from . import views

app_name = "reports"
urlpatterns = [
    path("create/", views.CreateReportView.as_view(), name="create"),
    path("<int:report_id>/", views.GetReportView.as_view(), name="get"),
]
