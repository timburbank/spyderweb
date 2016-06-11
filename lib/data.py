# Functions for interacting with the database

import sqlite3
import os
import config

env = "data env"

# Confirm we're in the right file
def database():
	print('Date a Bass?')

# params
# fields: list of ticket fields to retrieve
# filters: dictionary of field:value:comparison
# order: string, field to order by
# limit: int, how many items to retrieve
# ascending: bool, which way to order
def get_ticket_data(fields, filters = 0, order='id', ascending = 1, limit = 0):
	# unimplemented: order, ascending, limit
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	cursor = db.cursor()

	# get list of ids
	query = 'SELECT DISTINCT ticket_id FROM fields WHERE visible == 1'
	id_list_cursor  = cursor.execute(query)
	id_list = []
	for item in id_list_cursor:
		id_list.append(item[0])
		
	filtered_ticket_data = []
	for this_id in id_list:

		config_fields = config.fields()
		ticket_data = {}

		for field in config_fields:
			query = "SELECT * FROM fields \
			         WHERE ticket_id = '{}' \
			         AND name LIKE '{}' \
			         ORDER BY version DESC LIMIT 0,1"\
			         .format(this_id, field)
			cursor.execute(query)
			field_data = cursor.fetchone()
			
			# if field doesn't exist return default
			if field_data == None:
				default_value = config.field_default(field)
				ticket_data[field] = default_value
			else:
				ticket_data[field] = field_data[5]
		ticket_data['id'] = this_id

		# filter data
		pass_filters = True
		if filters:
			for filter in filters:
				key = str(filter[0]).strip()
				filter_value = str(filter[1]).strip()
				ticket_field_value = str(ticket_data[key]).strip()
				try:
					comparison = filter[2]
				except:
					comparison = '='

				if comparison is '=' and ticket_field_value != filter_value:
					pass_filters = False
				elif comparison is 'not' and ticket_field_value == filter_value:
					pass_filters = False
		if pass_filters:
			filtered_ticket_data.append(ticket_data)
			
	return(filtered_ticket_data)


# Returns highest version number of ticket
def get_version(ticket_id):
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
        cursor = db.cursor()

	
	query = "SELECT version \
	         FROM fields \
	         WHERE ticket_id = {} \
	         ORDER BY version DESC \
	         LIMIT 0,1"\
	         .format(ticket_id)
	cursor.execute(query)
	get_version = cursor.fetchone()[0]
	return(get_version)
	
# Writes ticket data to storage
# 
# param:
# data, library of key:value pairs to store
# id, int ID of ticket to write
def set_ticket_data(ticket_id, data):

	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	cursor = db.cursor()

	query = "SELECT version \
	         FROM fields \
	         WHERE ticket_id = {} \
	         ORDER BY version DESC \
	         LIMIT 0,1"\
	         .format(ticket_id)
	cursor.execute(query)
	last_version = cursor.fetchone()
	if last_version == None:
		new_version = 1
	else:
		new_version = last_version[0] + 1

	query_fields = ''
	query_content = ''
	for field, content in data.items():
		if content == "":
			content = config.field_default(field)
		if content is not "":
			query = "INSERT INTO fields (\
			             'ticket_id', \
			             'version', \
			             'name', \
			             'content') \
			         VALUES (?, ?, ?, ?)"
			# from http://stackoverflow.com/a/3952550
			db.execute(query,(ticket_id, new_version, field, content))

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
	query = 'SELECT DISTINCT ticket_id \
	         FROM fields \
	         ORDER BY ticket_id DESC \
	         LIMIT 0, 1'
	cursor = db.execute(query)
	id = 1
	for row in cursor:
		id = row[0] + 1

	db.close()
	set_ticket_data(id, data)
		
	return(id)

# setup database
def initialize():
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	# should use exceptions here? http://zetcode.com/db/sqlitepythontutorial/
	# Uf we need to push/pull field IDs maybe want to be hash?
	query = 'CREATE TABLE fields( \
		id INTEGER PRIMARY KEY, \
		timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, \
		ticket_id INT, \
		version INT, \
		name TEXT, \
		content TEXT, \
		visible INT DEFAULT 1\
		)'
	db.execute(query)
	db.commit()
	db.close()


def delete(ticket_id):
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	
	query = 'DELETE FROM fields WHERE ticket_id = {}'.format(ticket_id)
	db.execute(query)
	db.commit()
	db.close()

def hide(ticket_id):
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))

	query = "UPDATE fields SET visible = 0 WHERE ticket_id = {}"\
		.format(ticket_id)
	db.execute(query)

	db.commit()
	db.close()


def unhide(ticket_id):
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))

	query = "UPDATE fields SET visible = 1 WHERE ticket_id = {}"\
    	.format(ticket_id)
	db.execute(query)

	db.commit()
	db.close()


# update possible previous versions of the database
def upgrade():
	db = sqlite3.connect(os.path.join(env, 'spyderweb.db'))
	try:
		db.execute('ALTER TABLE fields ADD COLUMN visible INT DEFAULT 1')
		print('Database updated. "visible" field added')
	except:
		print('Database not updated (that probably means it\'s already good')
	
# sqlite stuff
# http://zetcode.com/db/sqlitepythontutorial/
# http://www.tutorialspoint.com/sqlite/sqlite_python.htm
# http://pythoncentral.io/introduction-to-sqlite-in-python/
	
