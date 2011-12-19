from django import forms
from blog.models import Article, Comment
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        exclude = ('user',)

class CommentForm(forms.ModelForm):
    article=None
    ip=None
    def __init__(self, *args, **kwargs):
        try:
            self.article=kwargs.pop('article')
            self.ip=kwargs.pop('ip')
        except:
            pass
        super(CommentForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model=Comment
        fields=('comment',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            comment=Comment.objects.get(article=self.article, comment=cleaned_data.get('comment'), ip=self.ip)
        except ObjectDoesNotExist:
            pass
        else:
           raise ValidationError("You already wrote the same comment for this article")
        return cleaned_data