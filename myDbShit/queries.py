#user details

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","idontknow","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM USERS \
       WHERE user_id = 'santhu'"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      user_id = row[0]
      passw = row[1]
      # Now print fetched result
      print "user_id=%s,pass=%s" % \
             (user_id, passw )
except:
   print "Error: unable to fecth data"

# disconnect from server
db.close()
