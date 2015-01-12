from django.shortcuts import render
import urllib2
from bs4 import BeautifulSoup
import feedparser
from django.http import HttpResponseRedirect, HttpResponse
import re
import urllib2

class QTopic :

  
  @staticmethod
  def get_related_topics (topic) :
   	url = "https://www.quora.com/" + topic 
	html_doc = urllib2.urlopen (url)
	soup = BeautifulSoup (html_doc.read ())
	raw_data = str (soup.find_all ('div', class_='RelatedTopicsSection row section related_topics'))
	soup = BeautifulSoup (raw_data)
	raw_data = str (soup.find_all ('span',class_='TopicName'))
	soup = BeautifulSoup (raw_data)
	related_topics = soup.get_text ()
	dict = {
		'topic' : topic,
		'related_topics' : related_topics,
	}
	return dict

	
  @staticmethod
  def get_best_questions (topic) :
   	url = "http://www.quora.com/" + topic + "/best_questions/rss"
	f = feedparser.parse (url)
	feed_len = len (f.entries)
	links = []
	title = []
	published = []
	for i in range (feed_len) :
		links.append (f['entries'][i]['links'][0]['href'])
		title.append (f['entries'][i]['title'])
		published.append (f['entries'][i]['published'])
	dict = {
		'links' : links,
		'title' : title,
		'published' : published
    }
	return dict

  @staticmethod
  def get_top_stories (topic) :
   	url = "http://www.quora.com/" + topic + "/rss"
	f = feedparser.parse (url)
	feed_len = len (f.entries)
	links = []
	title = []
	published = []
	for i in range (feed_len) :
		links.append (f['entries'][i]['links'][0]['href'])
		title.append (f['entries'][i]['title'])
		published.append (f['entries'][i]['published'])
	dict = {
		'links' : links,
		'title' : title,
		'published' : published
    }
	return dict
 
  @staticmethod
  def  get_open_questions (topic) :
	url = "http://www.quora.com/" + topic + "/questions"
	html_doc = urllib2.urlopen (url)
	soup = BeautifulSoup (html_doc.read ())
	raw_data = str (soup.find_all ('div',class_='QuestionText'))
	title=""
	for i in range(len(soup.find_all ('div',class_='QuestionText'))):
		result = soup.find_all ('div',class_='QuestionText')[i]
		title = title+"[][][][]"+ result.get_text()
	soup = BeautifulSoup (raw_data)
	dict = {
		'question_titles' : title,
		'topic' : topic,
	}
	return dict

  @staticmethod
  def dump_user_answers (topic) :
	url = "http://www.quora.com/" + topic + "/answers/rss"
	f = feedparser.parse (url)
	feed_len = len (f.entries)
	links = []
	title = []
	published = []
	description=[]
	for i in range (feed_len) :
		links.append (f['entries'][i]['links'][0]['href'])
		title.append (f['entries'][i]['title'])
		published.append (f['entries'][i]['published'])
		description.append (f['entries'][i]['description'])

	dict = {
		'links' : links,
		'title' : title,
		'published' : published,
		'description' : description
    }
	return dict

def test(request):
	username = request.GET['param']
	
	if 'www.quora.com/' not in str(username):
		return HttpResponse("Please be active on Quora homepage before using this extension.")

	else:
		mode=request.GET['mode']
		username=username.split("/")[3]
		if mode==u'0':
			return HttpResponse("Select your choice.")
		elif mode==u'1':
			best_questions = QTopic.get_best_questions (username)
			lo=len(best_questions['links'])
			strs=""
			for i in range(lo):
				strs=strs+"<a href="+str(best_questions['links'][i].encode('utf-8').strip())+">"+str(best_questions['title'][i].encode('utf-8').strip())+"</a>"+"<br>"+"<br>"
			return HttpResponse(strs)
		elif mode==u'2':
			open_questions = QTopic.get_open_questions (username)
			strs=""
			a = open_questions['question_titles'].split('[][][][]')
			lo=len(a)
			for i in range(lo):
				strs=strs+a[i]+"<br>"+"<br>"
			return HttpResponse(strs)

		elif mode==u'3':
			related_topics = QTopic.get_related_topics (username)
			lo=len(related_topics['related_topics'])
			strs=""
			a=related_topics['related_topics'].encode('utf-8').split(",")
			lo=len(a)
			for i in range(lo):
				a[i]=a[i].replace("[","")
				a[i]=a[i].replace("]","")
				strs=strs+str(a[i])+"<br>"+"<br>"
			return HttpResponse(strs)

		elif mode==u'4':
			top_stories = QTopic.get_top_stories (username)
			lo=len(top_stories['links'])
			strs=""
			for i in range(lo):
				strs=strs+"<a href="+str(top_stories['links'][i].encode('utf-8').strip())+">"+str(top_stories['title'][i].encode('utf-8').strip())+"</a>"+"<br>"+"<br>"+"\n"
			return HttpResponse(strs)

		elif mode==u'5':
			user_answers = QTopic.dump_user_answers (username)
			lo=len(user_answers['links'])
			strs=""
			for i in range(lo):
				strs=strs+"<a href="+str(user_answers['links'][i].encode('utf-8').strip())+">"+str(user_answers['title'][i].encode('utf-8').strip())+"</a>"+"<br>"+"<br>"+"\n"
			
			return HttpResponse(strs)

		