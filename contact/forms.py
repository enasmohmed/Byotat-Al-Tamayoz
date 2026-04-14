from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from core.models import SiteSettings
from projects.models import Project


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "name", "required": True}),
    )
    phone = forms.CharField(
        label=_("Phone"),
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel", "required": True}),
    )
    project = forms.ChoiceField(
        label=_("Project"),
        choices=(),
        widget=forms.Select(attrs={"class": "form-control", "required": True}),
    )
    project_status_current = forms.BooleanField(
        label=_("Current projects"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    project_status_under_construction = forms.BooleanField(
        label=_("Under-construction projects"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "required": True}),
    )
    send_via_whatsapp = forms.BooleanField(
        label=_("Via company WhatsApp"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, site=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.site = site if site is not None else SiteSettings.objects.first()
        self.is_arabic = (get_language() or "").startswith("ar")
        has_wa = bool(self.site and getattr(self.site, "whatsapp_digits", ""))

        if self.is_arabic:
            self.fields["project"].label = "المشروع"
            self.fields["phone"].label = "رقم الجوال"
            self.fields["project_status_current"].label = "المشاريع الحالية"
            self.fields["project_status_under_construction"].label = "مشاريع تحت الإنشاء"
            self.fields["send_via_whatsapp"].label = "عبر واتساب الشركة"

        self.fields["send_via_whatsapp"].initial = True
        if has_wa:
            self.fields["send_via_whatsapp"].widget = forms.HiddenInput()

        status_values = self._selected_status_values()
        self.fields["project"].choices = self._project_choices(status_values)

    def _selected_status_values(self):
        current_selected = True
        under_construction_selected = True
        if self.is_bound:
            current_selected = bool(self.data.get("project_status_current"))
            under_construction_selected = bool(self.data.get("project_status_under_construction"))

        statuses = []
        if current_selected:
            statuses.append(Project.ProjectStatus.CURRENT)
        if under_construction_selected:
            statuses.append(Project.ProjectStatus.UNDER_CONSTRUCTION)
        return statuses

    def _project_choices(self, statuses):
        choices = [("", "اختر المشروع" if self.is_arabic else _("Select a project"))]
        if not statuses:
            return choices

        projects = Project.objects.filter(is_active=True, status__in=statuses).order_by("-id")
        for project in projects:
            if self.is_arabic:
                if project.status == Project.ProjectStatus.CURRENT:
                    status_label = "الحالية"
                elif project.status == Project.ProjectStatus.UNDER_CONSTRUCTION:
                    status_label = "تحت الإنشاء"
                else:
                    status_label = "تم البيع"
            else:
                status_label = project.status_label_for_value(project.status)
            choices.append((str(project.pk), f"{project.title} ({status_label})"))
        return choices

    def clean(self):
        cleaned = super().clean()
        if not self.site:
            raise ValidationError(_("Site settings are missing. Please contact the administrator."))

        has_wa = bool(getattr(self.site, "whatsapp_digits", ""))
        selected_statuses = []
        if cleaned.get("project_status_current"):
            selected_statuses.append(Project.ProjectStatus.CURRENT)
        if cleaned.get("project_status_under_construction"):
            selected_statuses.append(Project.ProjectStatus.UNDER_CONSTRUCTION)

        if not selected_statuses:
            raise ValidationError(_("Please choose at least one project category: current or under construction."))

        project_id = cleaned.get("project")
        if not project_id:
            self.add_error("project", _("Please choose a project."))
        elif not Project.objects.filter(pk=project_id, is_active=True, status__in=selected_statuses).exists():
            self.add_error("project", _("Please choose a project that matches the selected categories."))

        if not has_wa:
            raise ValidationError(
                _("Company WhatsApp is not configured. Please ask the administrator to set it in Site settings.")
            )
        cleaned["send_via_whatsapp"] = True
        return cleaned
