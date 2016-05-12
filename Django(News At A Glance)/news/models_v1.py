# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import render
from pymongo import MongoClient
import jieba
import re
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
		for sli in jieba.cut(string, cut_all=False):
			if re.match(u'[\u4e00-\u9fa5]+', sli):  
				seg_array.append(sli);       
		return seg_array   
	
	
	def search(self,search_list): #定義多重條件查詢方法
		db=self.client.test       #databaseName
		collection=db.test        #tableName
		
		newsList=[]               #用來裝查詢結果
		line=""                   #用來裝查詢條件句子
		
		search_list = searchNews().str_slice(search_list) #呼叫str_slice()
		
		for i in xrange(0,len(search_list)):
			line += '{"content":{"$regex":\"'+search_list[i]+"\"}},"
		querry = '{"$and":['+line+"]}"  #組合完整句子
    
		for post in collection.find(eval(querry),{'_id':0}):
			newsList.append(post);
		return newsList
		client.close()
	
	#使用者輸入關鍵字後抓到的新聞存到newsList
	newsList = self.search();
	
	def clustering(self):
		newsList = self.newsList;   #拿到newsList變數裡面的東西
		
		
	
	
	
	
		
		
		
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