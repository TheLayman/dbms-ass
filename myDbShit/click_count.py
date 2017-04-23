#click_count

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","idontknow","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT click_count FROM click \
       WHERE user_id = 'bodd' AND video_id = '_8X1sQbil9A'"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      click_count = row
      # Now print fetched result
      print "click_count= %d " % \
             (click_count )
except:
   print "Error: unable to fecth data"

# disconnect from server
db.close()
