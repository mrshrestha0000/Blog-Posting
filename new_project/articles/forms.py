from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Article.objects.all().filter(title__icontains=title)
        if qs.exists():
            self.add_error("title", f"{title} is already in use")
        return data 

class ArticleFormOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean_title_content(self):
        cleaned_data = self.cleaned_data # dict
        print(cleaned_data)
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title.lower().strip() == "title1":
            raise forms.ValidationError('this title is already taken.')
        
        if content.lower().strip() == title:
            self.add_error('content', "content cannot be used in content")
        
        return title