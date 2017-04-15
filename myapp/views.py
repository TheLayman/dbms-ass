# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import SearchForm

import json
from utils import convert

from pymongo import MongoClient

connection = MongoClient()
db = connection.videos
videos = db.videos

## TODO write logic for first request.
def hello(request):
    vid_list = []
    if request.method == "POST":
       #Get the posted form
       form = SearchForm(request.POST)
       query = form['text'].value()
       ## TODO : write better query.
       for vid in videos.find({"videoInfo.snippet.title":{'$regex': query}}) :
           vid_list.append(vid)
           print(type(vid))
       return render(request, 'hello.html', {"vid_list" : vid_list})

    if request.method == "GET" :
       Id = request.GET.get("id")
       video = videos.find_one({ "videoInfo.id" : Id })
       for vid in videos.find({"videoInfo.snippet.title":{'$regex': ""}}) :
           vid_list.append(vid)
       return render(request, 'hello.html', {"current" : convert(video), "vid_list" : vid_list})

## TODO : Get trending videos and add to vid_list
def trending(request):
    vid_list = []
    if request.method == "GET" :
       for vid in videos.find({"videoInfo.snippet.title":{'$regex': ""}}).limit(10) :
           vid_list.append(vid)
       return render(request, 'hello.html', {"vid_list" : vid_list})

## TODO : Get PL videos and add to vid_list
def playList(request):
    vid_list = []
    if request.method == "GET" :
       for vid in videos.find({"videoInfo.snippet.title":{'$regex': ""}}).limit(10) :
           vid_list.append(vid)
       return render(request, 'hello.html', {"vid_list" : vid_list})

## Asyc request.
## TODO : Add video to playlist Database.
@csrf_exempt
def addToPlayList(request):
    if request.method == 'POST':
        videoId = request.POST.get('data', None)
        print("Added to PL : " + videoId)
        return HttpResponse(videoId)

## Asyc request.
## TODO : Add video to Liked Database add use it to recommend videos.
@csrf_exempt
def Like(request):
    if request.method == 'POST':
        videoId = request.POST.get('data', None)
        print("Liked : " + videoId)
        return HttpResponse(videoId)
