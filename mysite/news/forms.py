from django import forms

from .models import Category, News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'category': forms.Select(attrs={'class': 'form-select form-select-md mb-3'})
        }
        # fields = '__all__'


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
