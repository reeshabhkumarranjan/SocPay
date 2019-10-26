from django.forms import ModelForm
from .models import Groups


class GroupCreateForm(ModelForm):
    class Meta:
        model = Groups
        fields = ["group_name", "description", "fees"]
