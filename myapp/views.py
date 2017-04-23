# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import SearchForm, LoginForm, RegisterForm

import json
from utils import convert

from pymongo import MongoClient
from py2neo import Graph,Path,authenticate,Node,Relationship
from pprint import pprint
import MySQLdb
daba = MySQLdb.connect("localhost","root","iampavan","TESTDB")
cursor = daba.cursor()

authenticate("localhost:7474","neo4j","haha")
graph = Graph("http://localhost:7474/db/data/")
connection = MongoClient()
db = connection.videos
videos = db.videos


def register(request):
    if request.method == "POST":
       #Get the posted form
       form = RegisterForm(request.POST)
       username = form['username'].value()
       password = form['password'].value()
       args=(username,password)
       ## ADD to database and check if user already exists
       sql = "SELECT * FROM USERS WHERE user_id = \'"+username+"\'"
       cursor.execute(sql)
       if not cursor.rowcount:
           s = "INSERT INTO USERS  VALUES (%s,%s);"
           cursor.execute(s,args)
           daba.commit()
           request.session['LoginMessage'] = "Success! Please login Now."
           return redirect(login)
       else:
           request.session['LoginMessage'] = "You've already registered! Please login now"
           return redirect(login)



    if request.method == "GET":
        if request.session.has_key('username') and request.session['username'] != None :
           return redirect('/')
        else:
           return render(request, 'register.html', {"message" : "Please Signup"})

def login(request):
    success = False
    message = request.session.get('LoginMessage')
    if (message):
        del request.session['LoginMessage']
    else:
        message = ""

    if request.method == "POST":
       ## Get the posted form
       form = LoginForm(request.POST)
       username = form['username'].value()
       password = form['password'].value()
       ## Check Auth here.
       sql = "SELECT * FROM USERS WHERE user_id = \'"+username+"\' AND pass = \'"+password+"\';"
       try:
          cursor.execute(sql)
          if not cursor.rowcount:
              success=False
          else:
            success = True
       except:
           success=False
           return render(request, 'login.html', {"message" : "Systems Error, Please try again after sometime!"})
       if (success):
           request.session['username'] = username
           return redirect('/')
       else :
           return render(request, 'login.html', {"message" : "Incorrect Credentials!"})

    if request.method == "GET":
        if request.session.has_key('username') and request.session['username'] != None:
           return redirect('/')
        else:
           if message == "":
               message = "Login"
           return render(request, 'login.html', {"message" : message})


def logout(request):
   try:
       if (request.session.get('username') != None):
           del request.session['username']
   except:
       pass
   return redirect(login)


def hello(request):
    vid_list = []

    if request.method == "POST" :
       if request.session.has_key('username') and request.session['username'] != None :
            username = request.session.get('username')
            tip="SignOut"
       else:
           username="None"
           tip="Login"
       form = SearchForm(request.POST)
       query = form['text'].value()
       pipe=[{"$match":{"$text": {"$search": query} }}, {"$sort":{"score":{"$meta": "textScore"}}},{"$project":{"score":{"$meta":"textScore"},"videoInfo.id":1,"title":1,"desc":1,"videoInfo.snippet.thumbnails.default.url":1,"videoInfo.snippet.thumbnails.medium.url":1}}]
       for vid in videos.aggregate(pipeline=pipe):
           if request.session.has_key('username') and request.session['username']!= None:
                              sql = "SELECT click_count FROM click WHERE user_id = \'"+username+"\' AND video_id = \'"+str(vid['videoInfo']['id'])+"\';"
                              try:
                                 cursor.execute(sql)
                                 results = cursor.fetchall()
                                 for row in results:
                                    click_count = row
                                    score=0.2*float( "%d " % \
                                           (click_count ))
                                    vid['score']+=score
                              except:
                                 print "Error: unable to fecth data"
                              sql = "SELECT * FROM liked WHERE user_id = \'"+username+"\' AND video_id = \'"+str(vid['videoInfo']['id'])+"\';"
                              try:
                                 cursor.execute(sql)
                                 if not cursor.rowcount:
                                     vid['score']+=1
                              except:
                                 print "Error: unable to fecth data"
           vid_list.append(vid)
       if not vid_list:
           regex=".*" + query + ".*"
           for vid in videos.find({"title":{'$regex': regex, "$options": "-i"}}).limit(12) :
               vid_list.append(vid)
           if not vid_list:
                for vid in videos.find({"tags":{'$regex': regex, "$options": "-i"}}).limit(12) :
                    vid_list.append(vid)
                if not vid_list:
                    for vid in videos.find({"desc":{'$regex': regex, "$options": "-i"}}).limit(12) :
                        vid_list.append(vid)
           if not vid_list:
                  return render(request, 'home.html', {"vid_list" : vid_list, "username" : username,"blah":"No Results Found, Try Changing the query","tip":tip})
           return render(request, 'home.html', {"vid_list" : vid_list, "username" : username,"blah":"Search Results","tip":tip})
       newlist = sorted(vid_list, key=lambda k: k['score'],reverse=True)
       return render(request, 'home.html', {"vid_list" : newlist, "username" : username,"blah":"Search Results","tip":tip})
    if request.method == "GET" :
        if request.session.has_key('username') and request.session['username'] != None :
             username = request.session.get('username')
             tip="SignOut"
        else:
            username="None"
            tip="Login"
        Id = request.GET.get("id")
        if Id!=None:
            video = videos.find_one({ "videoInfo.id" : Id })
            videos.update({ "videoInfo.id" : Id },{'$inc':{"videoInfo.statistics.viewCount":1}})
            results = graph.run("MATCH (n)-[r]-(m) where n.id={x} return m.id order by r.weight desc limit 50", x=Id)
            for one in results:
                one=dict(one)
                vid=videos.find_one({ "videoInfo.id" : one['m.id'] })
                vid_list.append(vid)
            return render(request, 'play.html', {"current" : convert(video), "vid_list" : vid_list,
                                                  "username" : username,"tip":tip})
        if Id==None:#TODO: Without Login....With Login.
            for vid in videos.find().sort("videoInfo.statistics.viewCount",-1).limit(12) :
                vid_list.append(vid)

            return render(request, 'home.html', { "vid_list" : vid_list,
                                                  "username" : username,"blah":"Trending Videos","tip":tip})

def trending(request):
    username=request.session.get('username')
    vid_list = []
    if request.session.has_key('username') and request.session['username'] != None :
         username = request.session.get('username')
         tip="SignOut"
    else:
        tip="Login"
    if request.method == "GET" :
       for vid in videos.find().sort("videoInfo.statistics.viewCount",-1).limit(12) :
           vid_list.append(vid)
       return render(request, 'home.html', {"vid_list" : vid_list,"tip":tip})
    if request.method == "POST" :
           if request.session.has_key('username') and request.session['username'] != None :
                username = request.session.get('username')
                tip="SignOut"
           else:
               username="None"
               tip="Login"
           form = SearchForm(request.POST)
           query = form['text'].value()
           pipe=[{"$match":{"$text": {"$search": query} }}, {"$sort":{"score":{"$meta": "textScore"}}},{"$project":{"score":{"$meta":"textScore"},"videoInfo.id":1,"title":1,"desc":1,"videoInfo.snippet.thumbnails.default.url":1,"videoInfo.snippet.thumbnails.medium.url":1}}]
           for vid in videos.aggregate(pipeline=pipe):
               if request.session.has_key('username') and request.session['username']!= None:
                                  sql = "SELECT click_count FROM click WHERE user_id = \'"+username+"\' AND video_id = \'"+str(vid['videoInfo']['id'])+"\';"
                                  try:
                                     cursor.execute(sql)
                                     results = cursor.fetchall()
                                     for row in results:
                                        click_count = row
                                        score=0.2*float( "%d " % \
                                               (click_count ))
                                        vid['score']+=score
                                  except:
                                     print "Error: unable to fecth data"
                                  sql = "SELECT * FROM liked WHERE user_id = \'"+username+"\' AND video_id = \'"+str(vid['videoInfo']['id'])+"\';"
                                  try:
                                     cursor.execute(sql)
                                     if not cursor.rowcount:
                                         vid['score']+=1
                                  except:
                                     print "Error: unable to fecth data"
               vid_list.append(vid)
           if not vid_list:
               regex=".*" + query + ".*"
               for vid in videos.find({"title":{'$regex': regex, "$options": "-i"}}).limit(12) :
                   vid_list.append(vid)
               if not vid_list:
                    for vid in videos.find({"tags":{'$regex': regex, "$options": "-i"}}).limit(12) :
                        vid_list.append(vid)
                    if not vid_list:
                        for vid in videos.find({"desc":{'$regex': regex, "$options": "-i"}}).limit(12) :
                            vid_list.append(vid)
               if not vid_list:
                      return render(request, 'home.html', {"vid_list" : vid_list, "username" : username,"blah":"No Results Found, Try Changing the query","tip":tip})
               return render(request, 'home.html', {"vid_list" : vid_list, "username" : username,"blah":"Search Results","tip":tip})
           newlist = sorted(vid_list, key=lambda k: k['score'],reverse=True)
           return render(request, 'home.html', {"vid_list" : newlist, "username" : username,"blah":"Search Results","tip":tip})

def playList(request):
    vid_list = []
    newlist=[]
    if request.session.has_key('username') and request.session['username'] != None :
         username = request.session.get('username')
         tip="SignOut"
    else:
        tip="Login"
        return render(request, 'home.html', { "vid_list" : vid_list,"blah":"Please login to view your playlist","tip":tip})
    if request.method == "GET" :
       username=request.session.get('username')
       s="select * from playlist where user_id=\'"+username+"\';"
       cursor.execute(s)
       results = cursor.fetchall()
       for row in results:
          video_id = row[0]
          vid=videos.find_one({"videoInfo.id":video_id})
          vid_list.append(vid)
       return render(request, 'home.html', {"vid_list" : vid_list,"tip":tip,"dummy":10})
    if request.method == "POST" :
           if request.session.has_key('username') and request.session['username'] != None :
                username = request.session.get('username')
                tip="SignOut"
           else:
               username="None"
               tip="Login"
           form = SearchForm(request.POST)
           query = form['text'].value()
           pipe=[{"$match":{"$text": {"$search": query} }}, {"$sort":{"score":{"$meta": "textScore"}}},{"$project":{"score":{"$meta":"textScore"},"videoInfo.id":1,"title":1,"desc":1,"videoInfo.snippet.thumbnails.default.url":1,"videoInfo.snippet.thumbnails.medium.url":1}}]
           for vid in videos.aggregate(pipeline=pipe):
               if request.session.has_key('username') and request.session['username']!= None:
                                  sql = "SELECT click_count FROM click WHERE user_id = \'"+username+"\' AND video_id = \'"+str(vid['videoInfo']['id'])+"\';"
                                  try:
                                     cursor.execute(sql)
                                     results = cursor.fetchall()
                                     for row in results:
                                        click_count = row
                                        score=0.2*float( "%d " % \
                                               (click_count ))
                                        vid['score']+=score
                                  except:
                                     print "Error: unable to fecth data"
                                  sql = "SELECT * FROM liked WHERE user_id = \'"+username+"\' AND video_id = \'"+str(vid['videoInfo']['id'])+"\';"
                                  try:
                                     cursor.execute(sql)
                                     if not cursor.rowcount:
                                         vid['score']+=1
                                  except:
                                     print "Error: unable to fecth data"
               vid_list.append(vid)
           if not vid_list:
               regex=".*" + query + ".*"
               for vid in videos.find({"title":{'$regex': regex, "$options": "-i"}}).limit(12) :
                   vid_list.append(vid)
               if not vid_list:
                    for vid in videos.find({"tags":{'$regex': regex, "$options": "-i"}}).limit(12) :
                        vid_list.append(vid)
                    if not vid_list:
                        for vid in videos.find({"desc":{'$regex': regex, "$options": "-i"}}).limit(12) :
                            vid_list.append(vid)
               if not vid_list:
                      return render(request, 'home.html', {"vid_list" : vid_list, "username" : username,"blah":"No Results Found, Try Changing the query","tip":tip})
               return render(request, 'home.html', {"vid_list" : vid_list, "username" : username,"blah":"Search Results","tip":tip})
           newlist = sorted(vid_list, key=lambda k: k['score'],reverse=True)
           return render(request, 'home.html', {"vid_list" : newlist, "username" : username,"blah":"Search Results","tip":tip})

##   -- handle Users and Guests.
@csrf_exempt
def addToPlayList(request):
    #    s="select * from playlist where user_id=\'"+username+"\'AND video_id=\'"+video_id+"\';"
    if request.method == 'POST' and (request.session.get('username') != None):
        videoId = request.POST.get('data', None)
        username=request.session.get('username')
        args=(videoId,username)
        s = "INSERT INTO playlist  VALUES (%s,%s);"
        cursor.execute(s,args)
        try:
            daba.commit()
        except:
            daba.rollback()
        return HttpResponse(videoId)
    # else :
    #     return render(request, 'login.html', {"message" : "You must Login to like."})
## Asyc request.
##   -- handle Users and Guests.
@csrf_exempt
def Like(request):
    if request.method == 'POST'and (request.session.get('username') != None):
        videoId = request.POST.get('data', None)
        username=request.session.get('username')
        args=(videoId,username)
        s = "INSERT INTO liked  VALUES (%s,%s);"
        cursor.execute(s,args)
        try:
            daba.commit()
        except:
            daba.rollback()
        return HttpResponse(videoId)
    # else :
    #     return render(request, 'login.html', {"message" : "You must Login to like."})
