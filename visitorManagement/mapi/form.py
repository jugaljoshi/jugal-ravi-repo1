from visitorManagement.mapi.models import WorkBookType, Visitor
from django import forms


class WorkBookTypeAdminForm(forms.ModelForm):
    class Meta:
        model = WorkBookType
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data
        field_options = cleaned_data.get('field_options')
        if not field_options:
            raise forms.ValidationError("Field option can't be empty!")

        workbook_field_options_list = field_options.split(',')
        workbook_field_options_set = set(workbook_field_options_list)
        member_fields_set = Visitor._meta.get_all_field_names()
        while workbook_field_options_set:
            p = workbook_field_options_set.pop()
            if p not in member_fields_set:
                raise forms.ValidationError("%s doesn\'t exits in Visitor table!")
                break
        return super(WorkBookTypeAdminForm, self).clean()
