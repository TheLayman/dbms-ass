import MySQLdb
db = MySQLdb.connect("localhost","root","iampavan","TESTDB")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS USERS")
a = """CREATE TABLE USERS (
         user_id  CHAR(20) NOT NULL,
         pass  CHAR(20)	  NOT NULL,
	 CONSTRAINT returns_pk PRIMARY KEY ( user_id ))"""
cursor.execute(a)
b = """INSERT INTO USERS(user_id,pass)
         VALUES ('bodd','geo')"""
try:
   # Execute the SQL command
   cursor.execute(b)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
ab = """INSERT INTO USERS(user_id,pass)
         VALUES ('varma','wet')"""
cursor.execute(ab)
ac = """INSERT INTO USERS(user_id,pass)
         VALUES ('santhu','bhavana')"""
cursor.execute(ac)
ac = """INSERT INTO USERS(user_id,pass)
         VALUES ('mahi','ghanta')"""
cursor.execute(ac)

cursor.execute("DROP TABLE IF EXISTS playlist")
c = """CREATE TABLE playlist (
         video_id  CHAR(20) NOT NULL,
         user_id  CHAR(20)  NOT NULL,
	 CONSTRAINT returns_pk PRIMARY KEY ( user_id, video_id ))"""
cursor.execute(c)
q = """INSERT INTO playlist(video_id,user_id)
         VALUES ("4WfTlxXAL0",'bodd')"""
cursor.execute(q)
w= """INSERT INTO playlist(video_id,user_id)
         VALUES ("7Qdz_TpcE0",'bodd')"""
cursor.execute(w)
e = """INSERT INTO playlist(video_id,user_id)
         VALUES ("8X1sQbil9A",'bodd')"""
cursor.execute(e)
r = """INSERT INTO playlist(video_id,user_id)
         VALUES ("56kX-8pdxg",'bodd')"""
cursor.execute(r)
t = """INSERT INTO playlist(video_id,user_id)
         VALUES ("88fp0nLR40",'bodd')"""
cursor.execute(t)
y = """INSERT INTO playlist(video_id,user_id)
         VALUES ("0ziqk9cZRM",'bodd')"""
cursor.execute(y)
u = """INSERT INTO playlist(video_id,user_id)
         VALUES ("5kuoKHNxvc",'bodd')"""
cursor.execute(u)
i = """INSERT INTO playlist(video_id,user_id)
         VALUES ("7LDQ4hyIrw",'bodd')"""
cursor.execute(i)
o = """INSERT INTO playlist(video_id,user_id)
         VALUES ("8v1pkoDWs4",'bodd')"""
cursor.execute(o)

cursor.execute("DROP TABLE IF EXISTS click")
d = """CREATE TABLE click (
         video_id  CHAR(20) NOT NULL,
         user_id  CHAR(20)  NOT NULL,
	 query    CHAR(20)  NOT NULL,
	 click_count int    NOT NULL,
	 CONSTRAINT returns_pk PRIMARY KEY ( user_id, video_id, query ))"""
cursor.execute(d)

z = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("4WfTlxXAL0",'bodd','Handling ATMs',29)"""
cursor.execute(z)
x= """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("7Qdz_TpcE0",'bodd','Pathankot Attack',46)"""
cursor.execute(x)
v = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("8X1sQbil9A",'bodd','Bengali Rappers',65)"""
cursor.execute(v)
n = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("56kX-8pdxg",'bodd','Uri Attacks',12)"""
cursor.execute(n)
m = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("88fp0nLR40",'bodd','26/11/2008 ',39)"""
cursor.execute(m)
s = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("0ziqk9cZRM",'bodd','Darza Khulya Dekhum',90)"""
cursor.execute(s)
f = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("5kuoKHNxvc",'bodd','New Notes',32)"""
cursor.execute(f)
g = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("7LDQ4hyIrw",'bodd','Demonetisation',54)"""
cursor.execute(g)
h = """INSERT INTO click(video_id,user_id,query,click_count)
         VALUES ("8v1pkoDWs4",'bodd','Retaliatory Action',44)"""
cursor.execute(h)
try:
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()


# disconnect from server
db.close()
