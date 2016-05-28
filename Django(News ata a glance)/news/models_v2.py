# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import render
from pymongo import MongoClient
import jieba
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import sys
from sklearn import cluster
jieba.set_dictionary('E:/dics/dict.txt.big.txt') #結巴預設詞庫
jieba.load_userdict("E:/dics/dict_keyw.txt") #抽出新聞關鍵詞組成的詞庫

# Create your models here.

class newsinfo(object):
    def __init__(self):
        self.client= MongoClient('10.120.28.12', 27017)

    def getOnenewsInfo(self):
        db=self.client.test
        collection=db.test

        newsInfoList=[]
        for info in collection.find():
            newsInfoList.append(info)

        return newsInfoList

        client.close()

class searchNews(object):
	def __init__(self):
		self.client= MongoClient('10.120.28.12', 27017)
		
	def str_slice(self,string):  #定義切詞方法
		seg_array = []
		string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),string) #切詞
		for sli in jieba.cut(string, cut_all=False):
			if re.match(u'[\u4e00-\u9fa5]+', sli):  
				seg_array.append(sli)       
		return seg_array   
	
	
	def search(self,search_list): #定義多重條件查詢方法
		db=self.client.test       #databaseName
		collection=db.test2        #tableName
		
		newsList=[]               #用來裝查詢結果
		line=""                   #用來裝查詢條件句子
		
		search_list = searchNews().str_slice(search_list) #呼叫str_slice()
		
		for i in xrange(0,len(search_list)):
			line += '{"tfidf":{"$regex":\"'+search_list[i]+"\",'$options':'$i'}}," #會從tfidf的欄位去抓
		querry = '{"$and":['+line+"]}"  #組合完整句子
    
		for post in collection.find(eval(querry),{'_id':0}):
			newsList.append(post)
		return newsList
		client.close()
	
	
	def jieba_cut(self,search_list):
		
		#把使用者想找的新聞存到newsList
		newsList = searchNews().search(search_list)
		
		title = []
		content =[]
		for post in newsList: 
			summary = post['content']
			content.append('/'.join(jieba.cut(summary)))
			title.append(post['title'])
    
		#總文章數量
		count = len(content)
		
		return content,count,title,newsList
	
	def tfIdf_cluster(self,content,title):
		vectorizer = TfidfVectorizer()
		X = vectorizer.fit_transform(content)  
		weight = X.toarray()
		features = vectorizer.get_feature_names()
		
		c = cluster.KMeans(n_clusters=2)
		k_data = c.fit_predict(weight)  
		
		grp1_news = []
		grp2_news = []
		
		for idx, grp in enumerate(k_data):
			if grp == 0:
				grp1_news.append(title[idx])
			if grp == 1:
				grp2_news.append(title[idx])
		return weight,features,grp1_news,grp2_news
































#version1		
# class searchNews(object):
	# def __init__(self):
		# self.client= MongoClient('10.120.28.12', 27017)
	# def search(self,name):
		# db=self.client.test   #databaseName
		# collection=db.test    #tableName
		# newsList=[]
		# for post in collection.find({'tfidf':{'$regex':name}},{'_id':0}):
			# newsList.append(post)
		# return newsList
		# client.close() 