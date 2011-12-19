# -*- coding=utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


from django.utils.translation import ugettext_lazy as _
# Create your models here.




class Article(models.Model):
    title=models.CharField(max_length='255',verbose_name='Title')
    text=models.TextField(verbose_name='Text')
    slug=models.SlugField(verbose_name='Slug', max_length='255', unique=True)
    date=models.DateField(verbose_name='Date', auto_now_add=True)
    user=models.ForeignKey(User, verbose_name='User', null=True)
        
    def __unicode__(self):
        return self.title
     
    class Meta:
        verbose_name='Article'
        verbose_name_plural='Articles'
        

class Comment(models.Model):
    comment=models.TextField(verbose_name='Comment')
    date=models.DateTimeField(verbose_name='Date', auto_now_add=True)
    article=models.ForeignKey(Article, verbose_name='Article')
    user=models.ForeignKey(User, verbose_name='User', null=True)
    ip=models.IPAddressField(verbose_name='IP')
    
        
    def __unicode__(self):
        return self.comment
     
    class Meta:
        verbose_name='Comment'
        verbose_name_plural='Comments'
        
        
        
        