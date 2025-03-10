#!/usr/bin/python3 
import psycopg2, cgi 
import login
form = cgi.FieldStorage()

# Get values from the form in previous page 
name = form.getvalue('name')
id = form.getvalue('id')
iso_code = form.getvalue('iso_code')
birthdate = form.getvalue('birthdate')

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
	sql_person = "INSERT INTO person(id, name, iso_code) VALUES (%(id)s, %(name)s, %(iso_code)s)";
	sql_owner = "INSERT INTO owner(id, iso_code, birthdate) VALUES(%(id)s, %(iso_code)s, %(birthdate)s)";

	data_person = {'id':id,'name':name,'iso_code':iso_code}
	data_owner = {'id':id, 'iso_code':iso_code,'birthdate':birthdate}

        # Feed the data to the SQL query as follows to avoid SQL injection 
	cursor.execute(sql_person, data_person)
	cursor.execute(sql_owner, data_owner)
	print('Owner added successfully.')

	# Go back to homepage or add other 
	print('<p><a href="add_owner.cgi">Register another owner</a></p>')
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

