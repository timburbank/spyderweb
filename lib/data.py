# Functions for interacting with the database

import sqlite3
import os

env = "data env"

# Confirm we're in the right file
def database():
	print('Date a Bass?')

# params
# fields: list of ticket fields to retriev
# filters: dictionary of field:value:comparison
# order: string, field to order by
# limit: int, how many items to retrieve
# ascending: bool, which way to order
def get_ticket_data(fields, filters = 0, order='id', ascending = 1, limit = 0):
	temp_data_set = [ \
		{'id':1, 'name':'Garnet', 	'description':'We are the crystal gems',	'status':'todo'}, \
		{'id':2, 'name':'Amethyst', 'description':"We'll always save the day",	'status':'complete'}, \
		{'id':3, 'name':'Pearl', 	'description':"And if you think we can't",	'status':'workable'}, \
		{'id':4, 'name':'Stephen', 	'description':"We'll always find a way",	'status':'todo'} \
	]
	
	data = []
	for item in temp_data_set:
		datum = {}
		pass_filters = True	
		if(filters != 0):
			for key, value in filters.items():
				if (int(item[key]) == int(value)):
					pass_filters = True
				else:
					pass_filters = False
		if(pass_filters):
			for field in fields:
				datum[field] = item[field]
			data.append(datum)
		
		# need to implement filters
		
	return(data)
	
# Writes ticket data to storage
#
# param:
# data, library of key:value pairs to store
# id, int ID of ticket to write
def set_ticket_data(data, id):
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	
#	db.execute('INSERT INTO tickets (id) VALUES ({})'.format(id))

	print(data)
#	for content in data:
#		print('{}:{}'.format(content))

	db.commit()
	db.close()
	return(True)

# Creates new ticket
#
# param:
# data, library of key:value pairs for new ticket

# should we have create function, or just have set_ticket
#create a new entry if not given ID? create function is 
# probably more readable, but slightly more awkward
def create_ticket(data):
	# determine id

	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	cursor = db.execute('SELECT id FROM tickets ORDER BY id DESC LIMIT 0,1')
	id = 1
	for row in cursor:
		id = row[0] + 1

	db.close()
	set_ticket_data(data, id)
		
	return(id)

# setup database
def initialize():
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	db.execute("CREATE TABLE tickets(id INT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
	# should use exceptions here? http://zetcode.com/db/sqlitepythontutorial/

	db.execute('CREATE TABLE fields( \
		id INT, \
		timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, \
		ticket_id INT,\
		name TEXT, \
		)')
	db.commit()
	db.close()
	
# sqlite stuff
# http://zetcode.com/db/sqlitepythontutorial/
# http://www.tutorialspoint.com/sqlite/sqlite_python.htm
# http://pythoncentral.io/introduction-to-sqlite-in-python/
	
