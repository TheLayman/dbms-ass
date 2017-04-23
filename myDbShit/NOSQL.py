from glob import iglob
import os
import requests
import pymongo
import os.path
from pymongo import MongoClient
import json
from py2neo import Graph,Path,authenticate,Node,Relationship

def commoncount(list1,list2):
    count = 0
    for element in list1:
        if element in list2:
            count +=1
    return count

authenticate("localhost:7474","neo4j","haha")
graph = Graph("http://localhost:7474/db/data/")
array = []
i=0
for fname in iglob(os.path.expanduser('test/*.json')):
    with open(fname) as fin:
        videos = json.load(fin)
        array.append(videos)
        stats = videos['videoInfo']['statistics']
        node = Node("Video",id = videos['videoInfo']['id'], commentCount = stats['commentCount'], viewCount = stats['viewCount'], favoriteCount = stats['favoriteCount'], likeCount = int(stats['likeCount']) , dislikeCount = stats['dislikeCount'])
        graph.create(node)
print("Nodes Finished")

for i in range(len(array)):
    temp = array[i]['videoInfo']
    for j in range(i-1,-1,-1):
        dup = array[j]['videoInfo']
        a = graph.find_one("Video",property_key = 'id', property_value = temp['id'])
        b = graph.find_one("Video",property_key = 'id', property_value = dup['id'])
        if temp['snippet']['channelId'] == dup['snippet']['channelId']:
            crelation = Relationship(a,"samechannel",b, weight=5)
            graph.create(crelation)

        dcount = 1.5*commoncount(temp['snippet']['description'].split(),dup['snippet']['description'].split())
        if dcount != 0:
            drelation = Relationship(a , "similardescription" , b , weight = dcount)
            graph.create(drelation)

        if 'tags' in temp['snippet'] and 'tags' in dup['snippet']:
            tcount = 4*commoncount(temp['snippet']['tags'],dup['snippet']['tags'])
            if tcount != 0:
                trelation = Relationship(a, "similartags", b, weight = tcount)
                graph.create(trelation)

        ccount=10*commoncount(temp['snippet']['title'].split(),dup['snippet']['title'].split())
        if ccount != 0:
            crelation = Relationship(a , "similardescription" , b , weight = ccount)
            graph.create(crelation)
    print(i)


print("Neo4j...Finish")

# match (n)-[r]-(m) where n.id='5zG6AagUQBY' return m.id,r.weight order by r.weight desc limit 5;

connection = MongoClient()
db = connection.videos
videos = db.videos

for fname in iglob(os.path.expanduser('test/*.json')):
    with open(fname) as fin:
        videos = json.load(fin)
        title= videos['videoInfo']['snippet']['title']
        desc=videos['videoInfo']['snippet']['description']
        videos['title']=title
        videos['desc']=desc
        likeCount=videos['videoInfo']['statistics']['likeCount']
        videos['likeCount']=int(likeCount)
        del videos['videoInfo']['statistics']['likeCount']
        del videos['videoInfo']['snippet']['title']
        del videos['videoInfo']['snippet']['localized']['title']
        del videos['videoInfo']['snippet']['localized']['description']
        del videos['videoInfo']['snippet']['description']
        if 'tags' in videos['videoInfo']['snippet']:
            blah=videos['videoInfo']['snippet']['tags']
            videos['tags']=blah
            del videos['videoInfo']['snippet']['tags']
        ids=db.videos.insert(videos)
#db.videos.createIndex( { title: "text", desc: "text", tags:"text" }, { weights: { title: 20, tags:4, desc: 2 }, name: "TextIndex" } )
