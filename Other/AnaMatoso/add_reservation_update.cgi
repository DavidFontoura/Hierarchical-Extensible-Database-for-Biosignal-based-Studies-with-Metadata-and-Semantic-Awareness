#!/usr/bin/python3 
import psycopg2, cgi 
import login
form = cgi.FieldStorage()

# Get values from the form in previous page 
cni = form.getvalue('cni')
id_sailor = form.getvalue('id_sailor')
iso_code_sailor = form.getvalue('iso_code_sailor')
iso_code_boat = form.getvalue('iso_code_boat')
start_date = form.getvalue('start_date')
end_date = form.getvalue('end_date')

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Boat Management System</title>')
print('</head>')
print('<body>')
print('<h3>Confirmation of Update</h3>')

connection = None 
try:
        # Creating connection
	connection = psycopg2.connect(login.credentials) 
	cursor = connection.cursor()

        # Making query
	sql_schedule = "INSERT INTO schedule(start_date,end_date) VALUES (%(start_date)s,%(end_date)s)";
	sql = "INSERT INTO reservation(cni,iso_code_boat, id_sailor,iso_code_sailor,start_date,end_date) VALUES (%(cni)s, %(iso_code_boat)s, %(id_sailor)s,%(iso_code_sailor)s,%(start_date)s,%(end_date)s)";

	data = {'cni':cni,'iso_code_boat':iso_code_boat,'id_sailor':id_sailor,'iso_code_sailor':iso_code_sailor,'start_date':start_date,'end_date':end_date}
	data_schedule = {'start_date':start_date,'end_date':end_date}

        # Feed the data to the SQL query as follows to avoid SQL injection 
	cursor.execute(sql_schedule, data_schedule)
	cursor.execute(sql, data)
	print('Reservation added successfully.')

	# Go back to homepage or add other 
	print('<p><a href="add_reservation.cgi">Add another reservation</a></p>')
	print('<p><a href="homepage.cgi">Return to Homepage</a></p>')

        # Commit the update (without this step the database will not change) 
	connection.commit()

        # Closing connection
	cursor.close()

except Exception as e:
        # Print errors on the webpage if they occur 
	print('<h1>An error occurred.</h1>') 
	#print('<p>{}</p>'.format(e))
	print('<p> Please try again. Check if the values you wrote are valid.</p>')
finally:
	if connection is not None:
		connection.close()
print('</body>')
print('</html>')
