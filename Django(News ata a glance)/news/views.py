# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse  
from models import newsinfo     #className
from models import searchNews   #className
from django.shortcuts import render_to_response
import json
	


def index (request):
    return render(request,'index.html')	
	
	
def getnews(request,search):   #傳進來的參數search是長這樣search/，來自於url.py的url(r'(^search/$)'
	search_list=request.GET['name']  #一定要加['name']因為是要取GET物件的name屬性

	
	#抓分類好的新聞
	content,count,title,newsList,date,tfidf,sentence,pos_neg_json,trends,all_pos_word,all_neg_word = searchNews().jieba_cut(search_list)
	
	grp1_news,grp2_news,tfidf_word_grp1,tfidf_word_grp2= searchNews().tfIdf_cluster(content,title,date,tfidf)
	
	
	
	return render_to_response('post_list.html',locals())
	

def timeline (request,asp):   #傳進來的參數group是長這樣search/timeline，來自於url.py的url(r'(^search/timeline)'
	group = asp.split('/')[0] #使用者是點哪個group+關鍵詞
	
	search_list = asp.split('/')[1]
	
	content,count,title,newsList,date,tfidf,sentence,pos_neg_json,trends,all_pos_word,all_neg_word = searchNews().jieba_cut(search_list)
	
	grp1_news,grp2_news,tfidf_word_grp1,tfidf_word_grp2= searchNews().tfIdf_cluster(content,title,date,tfidf)
	
	return render_to_response('timeliner.html',locals())