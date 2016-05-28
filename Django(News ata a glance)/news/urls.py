from django.conf.urls import include, url
from django.contrib import admin
#from news.views import getnewsInfo
from . import views 

urlpatterns = [
	url(r'(^search/$)',views.getnews,name='getnews'),
	url(r'^$', views.index,name='index'),
	
	# url(r'(^search/timeline)', views.timeline,name='timeline'),
	url(r'(^search/timeliner/(?P<asp>.*)/$)', views.timeline,name='timeline'),
]