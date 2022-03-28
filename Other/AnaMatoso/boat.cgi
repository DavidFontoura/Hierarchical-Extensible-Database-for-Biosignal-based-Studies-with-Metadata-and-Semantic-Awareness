#!/usr/bin/python3
import psycopg2
import login
print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Boat Management System</title>')
print('</head>')
print('<body>')
print('<h3>Boat Management System</h3>')
connection = None
try:
        # Creating connection
	connection = psycopg2.connect(login.credentials)
	cursor = connection.cursor()
        # Print the register and remove buttons which will redirect to another page
	print('<p><a href="add_boat.cgi">Register Boat</a></p>')
	print('<p><a href="del_boat.cgi">Remove Boat</a></p>')

except Exception as e:
        # Print errors on the webpage if they occur
	print('<h1>An error occurred.</h1>')
	print('<p>{}</p>'.format(e))
finally:
	if connection is not None:
		connection.close()

print('</body>')

print('</html>')
