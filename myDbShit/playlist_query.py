#user_playlist

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","idontknow","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM playlist \
       WHERE user_id = 'bodd'"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      user_id = row[0]
      video_id = row[1]
      # Now print fetched result
      print "video_id=%s,user_id=%s" % \
             (user_id, video_id )
except:
   print "Error: unable to fecth data"

# disconnect from server
db.close()
