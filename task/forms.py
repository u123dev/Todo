import datetime
from django import forms
from django.core.exceptions import ValidationError

from task.models import Task, Tag


class TaskCreationForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    expected_deadline_date = datetime.date.today() + datetime.timedelta(days=5)
    deadline = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        required=False,
    )

    TRUE_FALSE_CHOICES = ((False, "No"), (True, "Yes"))
    is_done = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES,
        label="Is done ?",
        initial="",
        widget=forms.Select(), required=True)

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


def validate_deadline(deadline):
    if deadline and deadline < datetime.date.today():
        raise ValidationError(
            f"Deadline date should be not less than today: "
            f"{datetime.date.today().strftime("%d-%m-%Y")}"
        )

    return deadline
