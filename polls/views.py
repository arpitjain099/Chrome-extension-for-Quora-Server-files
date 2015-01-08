from django.shortcuts import render
import urllib2
from bs4 import BeautifulSoup
import feedparser
from django.http import HttpResponseRedirect, HttpResponse
import re
#import simplejson
#import wget
import urllib2
####################################################################
# API
####################################################################

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
	#print raw_data
	#link= str (soup.find_all ('div',class_='question_link'))
	#print len(soup.find_all ('div',class_='QuestionText'))
	title=""
	for i in range(len(soup.find_all ('div',class_='QuestionText'))):
		result = soup.find_all ('div',class_='QuestionText')[i]
		#print "The result of soup.find:"
		#print result

		#print "\nresult.contents:"
		#print result.contents
		#print "\nresult.get_text():"
		title = title+"[][][][]"+ result.get_text()
	soup = BeautifulSoup (raw_data)
	#print raw_data.contents
	#title = soup.get_text ()
	#title=title.replace(",","bhootkabaccha")
	#print title
	#print soup
	dict = {
		'question_titles' : title,
		'topic' : topic,
	#	'link':link
	}
	#dict['']
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

# Create your views here.
#def test(request):
#	return HttpResponse("Invalid login details supplied.")
def test(request):
    # Like before, obtain the context for the user's request.
    #context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    #if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        
        #password = request.POST['password']
        #password = 'Computer-Programming'
	#best_questions = QTopic.get_open_questions ('Computer-Programming')
	username = request.GET['param']
	
	if 'www.quora.com/' not in str(username):
		return HttpResponse("Please be active on Quora homepage before using this extension.")

	else:
		#return HttpResponse(username)		
		mode=request.GET['mode']
		#return HttpResponse(username)
		username=username.split("/")[3]
		#return HttpResponse(username)

		#print type(mode)
		#return HttpResponse(str(mode))
		if mode==u'0':
			return HttpResponse("Select your choice.")
		elif mode==u'1':
			#return HttpResponse("ffa")
			#username2='Computer-Programming'
			#return HttpResponse("balle balle")
			#return HttpResponse(username)
			best_questions = QTopic.get_best_questions (username)
			lo=len(best_questions['links'])
			#return HttpResponse("<a href='http://google.com'>Gooogle</a>")
			strs=""
			for i in range(lo):
	#print best_questions[i]['links']
				strs=strs+"<a href="+str(best_questions['links'][i].encode('utf-8').strip())+">"+str(best_questions['title'][i].encode('utf-8').strip())+"</a>"+"<br>"+"<br>"+"\n"
			#return HttpResponse(simplejson.dumps(a_best_questions))
			return HttpResponse(strs)

			#return HttpResponse(simplejson.dumps(best_questions))
		elif mode==u'2':
			#return HttpResponse("balle balle2")
			#return HttpResponse("ffa")
			#username2='Computer-Programming'
			#return HttpResponse("balle balle")
			#return HttpResponse(username)
			open_questions = QTopic.get_open_questions (username)
			#return HttpResponse(open_questions)
			#lo=len(open_questions['question_titles'])
			#return HttpResponse("<a href='http://google.com'>Gooogle</a>")
			strs=""
			a = open_questions['question_titles'].split('[][][][]')
			lo=len(a)
			#return HttpResponse(open_questions['question_titles'])
			for i in range(lo):
	#print best_questions[i]['links']
				#a[i].replace('[][][][]',',')
				strs=strs+a[i]+"\n"+"<br>"
			#return HttpResponse(simplejson.dumps(a_best_questions))
			return HttpResponse(strs)

		elif mode==u'3':
			#return HttpResponse("ffa")
			#username2='Computer-Programming'
			#return HttpResponse("balle balle")
			#return HttpResponse(username)
			related_topics = QTopic.get_related_topics (username)
			lo=len(related_topics['related_topics'])
			#return HttpResponse("<a href='http://google.com'>Gooogle</a>")
			strs=""
			a=related_topics['related_topics'].encode('utf-8').split(",")
			lo=len(a)
			for i in range(lo):
	#print best_questions[i]['links']
				a[i]=a[i].replace("[","")
				a[i]=a[i].replace("]","")
				strs=strs+str(a[i])+"<br>"+"<br>"
			#return HttpResponse(simplejson.dumps(a_best_questions))
			return HttpResponse(strs)

		elif mode==u'4':
			#return HttpResponse("ffa")
			#username2='Computer-Programming'
			#return HttpResponse("balle balle")
			#return HttpResponse(username)
			top_stories = QTopic.get_top_stories (username)
			lo=len(top_stories['links'])
			#return HttpResponse("<a href='http://google.com'>Gooogle</a>")
			strs=""
			for i in range(lo):
	#print best_questions[i]['links']
				strs=strs+"<a href="+str(top_stories['links'][i].encode('utf-8').strip())+">"+str(top_stories['title'][i].encode('utf-8').strip())+"</a>"+"<br>"+"<br>"+"\n"
			#return HttpResponse(simplejson.dumps(a_best_questions))
			return HttpResponse(strs)

		elif mode==u'5':
			#return HttpResponse("ffa")
			#username2='Computer-Programming'
			#return HttpResponse("balle balle")
			#return HttpResponse(username)
			user_answers = QTopic.dump_user_answers (username)
			lo=len(user_answers['links'])
			#return HttpResponse("<a href='http://google.com'>Gooogle</a>")
			strs=""
			for i in range(lo):
	#print best_questions[i]['links']
				strs=strs+"<a href="+str(user_answers['links'][i].encode('utf-8').strip())+">"+str(user_answers['title'][i].encode('utf-8').strip())+"</a>"+"<br>"+"<br>"+"\n"
			#return HttpResponse(simplejson.dumps(a_best_questions))
			return HttpResponse(strs)

		
				
		#return HttpResponse(mode)		
		#response_a = urllib2.urlopen(username)
		#page_source = response_a.read()
		#if "Top Stories" in page_source:
		#	return HttpResponse(page_source)
		#username=username.split("/")[1]






	#best_questions['name']
#best_questions['title']
#best_questions['published']
#print best_questions['links']
	#for i in best_questions['name']:
	#	print i
	#return HttpResponse(simplejson.dumps(best_questions))
	#return HttpResponse("fada")