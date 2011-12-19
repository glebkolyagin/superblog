from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from proj.blog import urls as blog_urls

# Uncomment the next two lines to enable the admin:

admin.autodiscover()

from proj.blog.views import main_page, get_article, add_article, edit_article, delete_article, mylogin, mylogout, reg


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proj.views.home', name='home'),s
    # url(r'^proj/', include('proj.foo.urls')),`

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    (r'^$', main_page),
    (r'^add/$', add_article),
    (r'^edit/([\d]+)/$', edit_article),
    (r'^delete/([\d]+)/$', delete_article),
	(r'^login/$',mylogin),
	(r'^logout/$', mylogout),
    (r'^reg/$', reg),
    url(r'^admin/', include(admin.site.urls)),
	(r'^([\w\d]+)/$', get_article),
	
	
    
    
)

