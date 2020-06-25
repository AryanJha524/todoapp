from django import forms
from .models import todoItem


class CreateItemForm(forms.ModelForm):
    class Meta:
        model = todoItem
        fields = ['item_text', 'completed', 'priority']
