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

authenticate("localhost:7474","neo4j","haha")
graph = Graph("http://localhost:7474/db/data/")
connection = MongoClient()
db = connection.videos
videos = db.videos


## TODO : Add users to DB
def register(request):
    if request.method == "POST":
       #Get the posted form
       form = RegisterForm(request.POST)
       username = form['username'].value()
       password = form['password'].value()
       ## ADD to database and check if user already exists,
       request.session['LoginMessage'] = "Congrats"
       return redirect(login)

    if request.method == "GET":
        if request.session.has_key('username') and request.session['username'] != None :
           return redirect('/myapp/hello/')
        else:
           return render(request, 'register.html', {"message" : "register"})

## TODO : Check auth from database
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
       if ( username == "karthik" and password == "password" ):
           success = True
       if (success):
           request.session['username'] = username
           return redirect('/myapp/hello/')
       else :
           return render(request, 'login.html', {"message" : "username and password combo doesn't exist"})

    if request.method == "GET":
        if request.session.has_key('username') and request.session['username'] != None:
           return redirect('/myapp/hello/')
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

## TODO write logic for first request.
##   -- handle Users and Guests.
def hello(request):
    vid_list = []
    username = request.session.get('username')
    if request.method == "POST":
       #Get the posted form
       form = SearchForm(request.POST)
       query = form['text'].value()
       ## TODO : write better query
#videos.find({ "$text": { "$search": query }},{ "score": { "$meta": "textScore" }}).sort([('score', {'$meta': 'textScore'})]):
       pipe=[{"$match":{"$text": {"$search": query} }}, {"$sort":{"score":{"$meta": "textScore"}}},{"$project":{"score":{"$meta":"textScore"},"videoInfo.id":1,"title":1,"desc":1}}]
       for vid in videos.aggregate(pipeline=pipe):
           vid_list.append(vid)
       return render(request, 'hello.html', {"vid_list" : vid_list, "username" : username})


    if request.method == "GET" :
        Id = request.GET.get("id")
        if Id!=None:
            video = videos.find_one({ "videoInfo.id" : Id })
            results = graph.run("MATCH (n)-[r]-(m) where n.id={x} return m.id order by r.weight desc limit 10", x=Id)
            for one in results:
                one=dict(one)
                vid=videos.find_one({ "videoInfo.id" : one['m.id'] })
                vid_list.append(vid)
            return render(request, 'hello.html', {"current" : convert(video), "vid_list" : vid_list,
                                                  "username" : username})
        if Id==None:#Without Login....With Login.
            for vid in videos.find().sort("likeCount",-1) :
                vid_list.append(vid)
            return render(request, 'hello.html', { "vid_list" : vid_list,
                                                  "username" : username})
## TODO : Get trending videos and add to vid_list
def trending(request):
    vid_list = []
    if request.method == "GET" :
       for vid in videos.find().sort("videoInfo.statistics.viewCount",-1).limit(10) :
           vid_list.append(vid)
       return render(request, 'hello.html', {"vid_list" : vid_list})

## TODO : Get PL videos and add to vid_list
##   -- handle Users and Guests.
def playList(request):
    vid_list = []
    if request.method == "GET" :
       for vid in videos.find({"videoInfo.snippet.title":{'$regex': ""}}).limit(10) :
           vid_list.append(vid)
       return render(request, 'hello.html', {"vid_list" : vid_list})

## Asyc request.
## TODO : Add video to playlist Database.
##   -- handle Users and Guests.
@csrf_exempt
def addToPlayList(request):
    if request.method == 'POST':
        videoId = request.POST.get('data', None)
        print("Added to PL : " + videoId)
        return HttpResponse(videoId)

## Asyc request.
## TODO : Add video to Liked Database add use it to recommend videos.
##   -- handle Users and Guests.
@csrf_exempt
def Like(request):
    if request.method == 'POST':
        videoId = request.POST.get('data', None)
        print("Liked : " + videoId)
        return HttpResponse(videoId)
