# usings separate forms module helps make codebase tidier and easier to work with.
from django import forms 
from rango.models import Category, Page

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text = "Please enter the category name...")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    slug = forms.CharField(widget = forms.HiddenInput(), required = False )

    # an inline class to provide more information on the form 
    class Meta:
        # provide an association between the ModelForm and a model 
        model = Category
        fields = ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text = "please enter the title of the page ...")
    url = forms.URLField(max_length = 200, help_text = "Enter the url of the page here ...")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url 
            return cleaned_data
        
        
    class Meta:
        # provide an association between the ModelForm and a model 
        model = Page
        exclude = ('category', )