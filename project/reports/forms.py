from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime

from bootstrap4.widgets import RadioSelectButtonGroup

JUSTICE_CHOICES = (("not_guilty", "Не виновен"), ("guilty", "Виновен"))


class ReportForm(forms.Form):
    """Form with a variety of widgets to test bootstrap4 rendering."""

    client = forms.CharField(
        max_length=50,
        help_text="ФИО Клиента",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Иванов Иван Иванович"}),
    )

    case_number = forms.IntegerField(
        help_text="Номер дела",
        required=True,

        widget=forms.NumberInput(
            attrs={"placeholder": "123"}),
    )

    case_result = forms.ChoiceField(choices=JUSTICE_CHOICES, required=True, help_text="Приговор",)
    comment = forms.CharField(required=False, help_text="Комментарий",
                              widget=forms.TextInput(attrs={"placeholder": ""}),)

    required_css_class = "bootstrap4-req"

    def clean(self):
        cleaned_data = super().clean()
        # raise forms.ValidationError(
        #     "This error was added to show the non field errors styling.")
        return cleaned_data

    def generate_report_data(self):
        return self.cleaned_data
