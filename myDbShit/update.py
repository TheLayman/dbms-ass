#updating_clicks
#expects video_id, user_id, query
import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","idontknow","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

a = "SELECT click_count FROM click \
       WHERE user_id = 'bodd' AND video_id = 'aaa'"
cursor.execute(a)
results = cursor.fetchall()
print results

if results:
# Prepare SQL query to insert required records
	b = "UPDATE click SET click_count = click_count + 1 WHERE user_id = 'bodd' AND video_id = 'aaa'"
	cursor.execute(b)
	print "incremented"


else :



	v = """INSERT INTO click(video_id,user_id,query,click_count) VALUES ("aaa",'bodd','query',1)"""
	cursor.execute(v)


db.commit()

# disconnect from server
db.close()
