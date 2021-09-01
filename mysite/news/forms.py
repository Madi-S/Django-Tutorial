import re
from django import forms
from django.core.exceptions import ValidationError

from .models import Category, News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'category': forms.Select(attrs={'class': 'form-select form-select-md mb-3'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if str_starts_with_digit(title):
            raise ValidationError('Title should not start with a digit')
        return title
    

class _NewsForm(forms.Form):
    title = forms.CharField(
        max_length=150,
        label='News title',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        required=False,
        label='News content',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 7})
    )
    is_published = forms.BooleanField(
        initial=True,
        label='Active',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-label'})
    )
    category = forms.ModelChoiceField(
        label='News category',
        empty_label='Select category',
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-md mb-3'})
    )


def str_starts_with_digit(string):
    return re.match(r'\d', string)
