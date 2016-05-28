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
import json
jieba.set_dictionary('E:/dics/dict.txt.big.txt') #結巴預設詞庫
jieba.load_userdict("E:/dics/dict_keyw.txt") #抽出新聞關鍵詞組成的詞庫

# Create your models here.

class newsinfo(object):
    def __init__(self):
        self.client= MongoClient('10.120.28.12', 27017)

     #def getOnenewsInfo(self):
         #db=self.client.test
         #collection=db.test2

        # newsInfoList=[]
        # for info in collection.find():
            # newsInfoList.append(info)

        # return newsInfoList

        # client.close()

class searchNews(object):
	def __init__(self):
		self.client= MongoClient('10.120.28.12', 27017)
		
	def str_slice(self,string):  #定義切詞方法
		seg_array = []
		string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),string) #切詞
		sentence = ""     #抓出切好的句子並組起來，之後要放到頁面上
		for sli in jieba.cut(string, cut_all=False):
		
			sentence += sli+" "
			seg_array.append(sli)       
		return seg_array, sentence   
	
	
	def search(self,search_list): #定義多重條件查詢方法
		db=self.client.test       #databaseName
		collection=db.news2      #tableName
		
		newsList=[]               #用來裝查詢結果
		line=""                   #用來裝查詢條件句子
		pos_neg_json = []         #存取情緒json資料
		
		search_list, sentence = searchNews().str_slice(search_list) #呼叫str_slice()
		
		# for i in xrange(0,len(search_list)):
			# line += '{"tfidf":{"$regex":\"'+search_list[i]+"\",'$options':'$i'}}," #會從tfidf的欄位去抓
		# querry = '{"$and":['+line+"]}"  #組合完整句子
		
		
		for i in xrange(0,len(search_list)):
			line += '{"tfidf":\"'+search_list[i]+'\"},' #會從tfidf的欄位去抓
		querry = '{"$and":['+line+"]}"  #組合完整句子
		
		
		
		
		
		#存取搜尋過後的全部新聞資料--------------------------------------------------------------
		for post in collection.find(eval(querry),{'_id':0}).sort("date",1):
			newsList.append(post)
		#存取搜尋過後的全部新聞資料--------------------------------------------------------------
		
	
		#存取情緒曲線圖json資料-------------------------------------------
		collection2=db.ptt      #tableName
		for post in collection2.find(eval(querry),{'_id':0}).sort("date",1):

			
		
			dic1 = {
				'Date':post['date'],
				'Hot':len(post['pos']),
				'Channel':"Positive",
				'Title':post['title'],
			}
			dic2 = {
				'Date':post['date'],
				'Hot':len(post['neg']),
				'Channel':"Negative",
				'Title':post['title'],
			}
			pos_neg_json.append(dic1)
			pos_neg_json.append(dic2)
		pos_neg_json = json.dumps(pos_neg_json) #把 pos_neg_json 轉成json 的物件，之後要丟到javascript裡面使用
		#存取情緒曲線圖json資料結束---------------------------------------
			
		#存取情緒詞資料---------------------------------------
		
		all_pos_word=[]           #用來裝正向詞跟數量
		all_pos=[]                #用來裝所有正向詞
		for post in collection2.find(eval(querry),{'_id':0}).sort("date",1):
			pos = post['pos']
			for i in pos:
				all_pos.append(i)
		pos_dic = {}
		for ele in all_pos: # n
			if not ele in pos_dic:
				pos_dic[ele] = 1
			else:
				pos_dic[ele] = pos_dic[ele] + 1
		for i in range(0,len(pos_dic)):
			data = {
				"pos":pos_dic.keys()[i],
				"count":pos_dic.values()[i]
			}
			all_pos_word.append(data)
		all_pos_word.sort(key=lambda d:d['count'],reverse=True)   #幫情緒字進行排序
		
		#---------------------------------------------------------------------------------------------
		all_neg_word=[]           #用來裝負向詞跟數量
		all_neg=[]                #用來裝所有負向詞
		for post in collection2.find(eval(querry),{'_id':0}):
			neg = post['neg']
			for i in neg:
				all_neg.append(i)
		neg_dic = {}
		for ele in all_neg: # n
			if not ele in neg_dic:
				neg_dic[ele] = 1
			else:
				neg_dic[ele] = neg_dic[ele] + 1
		for i in range(0,len(neg_dic)):
			data = {
				"neg":neg_dic.keys()[i],
				"count":neg_dic.values()[i]
			}
			all_neg_word.append(data)
		all_neg_word.sort(key=lambda d:d['count'],reverse=True)   #幫情緒字進行排序
		
		#存取情緒詞資料結束---------------------------------------
			
		#新聞數量曲線圖trends---------------------------------------------
		date_list = collection.aggregate([
			{"$match":                                        #$match:設定查詢條件的字典
			 eval(querry)},
			{"$group":{"_id":"$date","daycount":{"$sum":1},"title":{"$first":"$title"}}},    #$group:設定group by的欄位, 計算筆數
			{"$sort":{"_id":1}}                               #查詢結果排序
			])
			
		date_list2 = collection2.aggregate([
			{"$match":                                        #$match:設定查詢條件的字典
			 eval(querry)},
			{"$group":{"_id":"$date","daycount":{"$sum":1},"title":{"$first":"$title"}}},    #$group:設定group by的欄位, 計算筆數
			{"$sort":{"_id":1}}                               #查詢結果排序
			])	

		
		all_json = []		
		for ele in date_list:
			
			c = ele["daycount"]		#當日的升量總和
			d = ele["_id"]          #當日
			e = ele["title"]
			
			data1 = {"date":d,
					"daycount":c,
					"title":e,
					"Channel":"News",
			}
				
			all_json.append(data1)

		for ele in date_list2:
			
			c = ele["daycount"]		#當日的升量總和
			d = ele["_id"]          #當日
			e = ele["title"]
			
			data2 = {"date":d,
					"daycount":c,
					"title":e,
					"Channel":"PTT",
			}
				
			all_json.append(data2)

		trends = json.dumps(all_json) 
		#新聞數量曲線圖trends結束---------------------------------------
		


			
		return newsList,sentence,pos_neg_json,trends,all_pos_word,all_neg_word
		client.close()
		
	
	def jieba_cut(self,search_list):
		
		#把使用者想找的新聞存到newsList
		newsList,sentence,pos_neg_json,trends,all_pos_word,all_neg_word = searchNews().search(search_list)
		

		title = []
		content =[]
		date= []
		tfidf=[]
		for post in newsList: 
			summary = post['content']
			content.append(' '.join(jieba.cut(summary)))
			title.append(post['title'])
			date.append(post['date'])
			tfidf.append(post['tfidf'])
    
		#總文章數量
		count = len(content)
		
		return content,count,title,newsList,date,tfidf,sentence,pos_neg_json,trends,all_pos_word,all_neg_word
	
	def tfIdf_cluster(self,content,title,date,tfidf):
		vectorizer = TfidfVectorizer()
		X = vectorizer.fit_transform(content)  
		weight = X.toarray()
		features = vectorizer.get_feature_names()
		
		c = cluster.KMeans(n_clusters=2)
		k_data = c.fit_predict(weight)  
		
		grp1_news = []
		grp2_news = []
		
		#把抓到的新聞存成[{},{}] key & value 的樣子方便前端取用
		# i = 0 
		for idx, grp in enumerate(k_data):
		
			if grp == 0:
				news =  {
					'title':title[idx],
					'date':date[idx],
					'content':''.join(content[idx].split()),
					'tfidf':tfidf[idx],
				}
				grp1_news.append(news)

			
			if grp == 1:
				news =  {
					'title':title[idx],
					'date':date[idx],
					'content':''.join(content[idx].split()),
					'tfidf':tfidf[idx],
				}
				grp2_news.append(news)
				
		#存取新聞分群TFIDF詞數量開始------------------------------------
		tfidf_word_grp1=[]           #用來裝TFIDF詞跟數量
		all_tfidf_grp1=[]                #用來裝所有TFIDF詞
		for post in grp1_news:
			tfidf = post['tfidf']
			for i in tfidf:
				all_tfidf_grp1.append(i)
		tfidf_dic1 = {}
		for ele in all_tfidf_grp1: # n
			if not ele in tfidf_dic1:
				tfidf_dic1[ele] = 1
			else:
				tfidf_dic1[ele] = tfidf_dic1[ele] + 1
		for i in range(0,len(tfidf_dic1)):
			data = {
				"text":tfidf_dic1.keys()[i],
				"size":(tfidf_dic1.values()[i])*2,
			}
			tfidf_word_grp1.append(data)
		
		tfidf_word_grp1.sort(key=lambda d:d['size'],reverse=True)   #幫情緒字進行排序
		
		tfidf_word_grp1 = tfidf_word_grp1[0:50]
		tfidf_word_grp1 = json.dumps(tfidf_word_grp1)
		
		#---------------------------------------------------------------------------------------------
		tfidf_word_grp2=[]           #用來裝TFIDF詞跟數量
		all_tfidf_grp2=[]                #用來裝所有TFIDF詞
		for post in grp2_news:
			tfidf = post['tfidf']
			for i in tfidf:
				all_tfidf_grp2.append(i)
		tfidf_dic2 = {}
		for ele in all_tfidf_grp2: # n
			if not ele in tfidf_dic2:
				tfidf_dic2[ele] = 1
			else:
				tfidf_dic2[ele] = tfidf_dic2[ele] + 1
		for i in range(0,len(tfidf_dic2)):
			data = {
				"text":tfidf_dic2.keys()[i],
				"size":(tfidf_dic2.values()[i])*2,
			}
			tfidf_word_grp2.append(data)
		tfidf_word_grp2.sort(key=lambda d:d['size'],reverse=True)   #幫情緒字進行排序
		tfidf_word_grp2 = tfidf_word_grp2[0:50]
		tfidf_word_grp2 = json.dumps(tfidf_word_grp2)	
		
		#存取新聞分群TFIDF詞數量結束------------------------------------
			
		return weight,features,grp1_news,grp2_news,tfidf_word_grp1,tfidf_word_grp2
































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