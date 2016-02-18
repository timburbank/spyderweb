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
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	cursor = db.cursor()

	# get list of ids

	if filters and 'id' in filters:
		id_list = [filters['id']]
	else:
		query = 'SELECT "id" FROM tickets'
		id_list_cursor  = cursor.execute(query)
		id_list = []
		for item in id_list_cursor:
			id_list.append(item[0])
		
	get_ticket_data = []
	for this_id in id_list:
		# this is not gonna work with more than one version of fields
		# what if: for field in config.fields: SELECT * FORM FIELDS WHERE
		#    ticked_id = $id AND name = $field ORDER BY VERSION DESC LIMIT 1
		query = 'SELECT * FROM fields WHERE ticket_id = {}'.format(this_id)
		cursed_fields = db.execute(query)
		ticket_data = {}
		# this will end badly if order of fields ever changes
		for field in cursed_fields:
			ticket_data[field[3]] = field[4]
			ticket_data['id'] = field[2]
		get_ticket_data.append(ticket_data)		
	return(get_ticket_data)		

# this might be helpful for when we actually implement filters
'''

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
'''		
	
# Writes ticket data to storage
#
# param:
# data, library of key:value pairs to store
# id, int ID of ticket to write
def set_ticket_data(ticket_id, data):
	# this (not surprisingly) is great for creating new tickets
	# but does bad things if they already exit because it just
	# adds new entries. This is kinda what we'll need for versioning
	# so maybe just go with it



	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	cursor = db.cursor()

	# if id doesn't exist, create a new one	
	cursor.execute("SELECT count(*) FROM tickets WHERE id = {}".format(ticked_id))
	ticket_exists = cursor.fetchone()[0]
	if ticket_exists == 0:
		db.execute('INSERT INTO tickets (id) VALUES ({})'.format(ticket_id))
		
	# TODO: determine new version number
	cursor.execute("SELECT version FROM fields WHERE ticket_id = {} ORDER BY version DESC LIMIT 1,1")
	

	# TODO: get fields from config

	# TODO: submit a query for each field (following code is wrong)
	query_fields = ''
	query_content = ''
	for field, content in data.items():
		db.execute('INSERT INTO fields ("ticket_id", "name", "content") VALUES ("{}", "{}", "{}")'.format(ticket_id, field, content))
# works but doesn't creat ID??

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
	set_ticket_data(id, data)
		
	return(id)

# setup database
def initialize():
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	db.execute("CREATE TABLE tickets(id INT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
	# should use exceptions here? http://zetcode.com/db/sqlitepythontutorial/
	# Uf we need to push/pull field IDs maybe want to be hash?
	db.execute('CREATE TABLE fields( \
		id INTEGER PRIMARY KEY, \
		timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, \
		ticket_id INT, \
		version INT,
		name TEXT, \
		content TEXT\
		)')
	db.commit()
	db.close()
	
# sqlite stuff
# http://zetcode.com/db/sqlitepythontutorial/
# http://www.tutorialspoint.com/sqlite/sqlite_python.htm
# http://pythoncentral.io/introduction-to-sqlite-in-python/
	
