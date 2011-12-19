from django.shortcuts import render_to_response
from django.template import RequestContext
from blog.models import Article, Comment
from blog.forms import ArticleForm, CommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.sweet_pagination import MyPage, get_page_list


def reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                logout(request.user)
            form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request,new_user)
            return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render_to_response("reg.html", {
        'form': form,
    },context_instance=RequestContext(request))
    
    
def mylogin(request):
	flag_no_auth = False
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(request.POST['next'])
			else:
				return render_to_response("login.html", {'username': request.POST['username'], 'no_active': True,}, context_instance=RequestContext(request))
		else:
			return render_to_response("login.html", {'username': request.POST['username'], 'error': True,}, context_instance=RequestContext(request))
	else:
		return render_to_response("login.html", {}, context_instance=RequestContext(request))
    
def mylogout(request):
	try:
		logout(request)
		return HttpResponseRedirect(request.GET['next'])
	except:
		return HttpResponseRedirect('/')
       
       
       
       
def main_page(request):
    try:
        articles=Article.objects.order_by("-date","-id")
    except ObjectDoesNotExist:
        articles=()
    
    
    paginator = Paginator(articles, 5) 
    
    
    page = request.GET.get('page')
    if page==None:
        page=1
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    
   
    page_list=get_page_list(paginator,10,page)

    return render_to_response("blog/index.html", {'articles': articles, 'page_list':page_list,}, 
    context_instance=RequestContext(request))
    
    

def get_article(request,slug):
    try:
        article=Article.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/')

    try:
        comments=Comment.objects.filter(article=article).order_by('-date','-id')        
    except ObjectDoesNotExist:
        comments=None
   
    if request.method == 'POST': 
        form = CommentForm(request.POST, **{'article':article,'ip':request.META['REMOTE_ADDR'],})
        if form.is_valid(): 
            comment=Comment()
            comment.comment = form.cleaned_data['comment']
            comment.article = article
            if request.user.is_authenticated():
                comment.user = request.user
            comment.ip=request.META['REMOTE_ADDR']
            comment.save()
            return HttpResponseRedirect('/'+article.slug) 
    else:
        form = CommentForm() 

    
    return render_to_response('blog/article.html', {
        'form': form,
        'article': article,
        'comments':comments,
    },context_instance=RequestContext(request))
        
    

    

    
def add_article(request):
    if request.method == 'POST': 
        if not request.user.is_authenticated() or not request.user.is_staff or not request.user.is_active:
            return HttpResponseRedirect('/')
            
        form = ArticleForm(request.POST)
        if form.is_valid(): 
            title = form.cleaned_data['title']
            slug = form.cleaned_data['slug']
            text = form.cleaned_data['text']
            article=Article(title=title, slug=slug, text=text, user=request.user)
            article.save()
            return HttpResponseRedirect('/')
    else:
        form = ArticleForm() 
    return render_to_response('blog/add_article.html', {
        'form': form,
         
    },context_instance=RequestContext(request))
    
    
def edit_article(request, id):
    next=get_next(request)
    
    try:
        article=Article.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(next)
        
    if request.method == 'POST': 
        if not request.user.is_authenticated() or not request.user.is_staff or not request.user.is_active: 
            return HttpResponseRedirect('/')
        if request.user!=article.user:
            return HttpResponseRedirect('/')
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect(next) 
    else:
        form = ArticleForm(instance=article) 
    return render_to_response('blog/edit_article.html', {
        'form': form,
        'article': article,
        'next': next,
    },context_instance=RequestContext(request))
    
    
def delete_article(request, id):

    next=get_next(request)
    
    try:
        article=Article.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(next)

    try:
        comments=Comment.objects.filter(article=article)
    except ObjectDoesNotExist:
        pass        
    
    if request.method == 'POST':
        if not request.user.is_authenticated() or not request.user.is_staff or not request.user.is_active:
            return HttpResponseRedirect('/')
        if request.user!=article.user:
            return HttpResponseRedirect('/')
        
        try:
            yes=request.POST['yes']
            if comments!=None:
                comments.delete()
            article.delete()
            return HttpResponseRedirect(next)
        except MultiValueDictKeyError:
            pass
            
        try:
            no=request.POST['no']
            return HttpResponseRedirect(next)
        except MultiValueDictKeyError:
            pass
        
        return HttpResponseRedirect(next)
    return render_to_response('blog/delete_article.html', { 'article': article, 'comments': comments, 'next':next, },
        context_instance=RequestContext(request)
        )
      


      
def get_next(request):
    next=''
    try:
        next=request.POST['next']
    except MultiValueDictKeyError:
        pass

    try:
        next=request.GET['next']
    except MultiValueDictKeyError:
        pass
    
    if next=='':
        next='/'
    
    return next
  
  
  
