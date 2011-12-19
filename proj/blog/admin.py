from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.contrib import admin

from django.http import HttpResponse
from django.core import serializers

   
from blog.models import Article, Comment

admin.site.register(Article)
admin.site.register(Comment)


