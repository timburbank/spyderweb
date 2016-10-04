# Functions for interacting with the database

import os
from . import config

env = "data env"

from sys import version_info
py3 = version_info[0] > 2
if py3:
	import configparser
else:
	import ConfigParser as configparser

# figure out what kind of data storage we're using, then pass the requested
# function on to the appropriate module

# We're evil and use a global var for the data module so we don't have
# to figure it out every time we call a data function
active_data = False

def set_data_storage():

	try:
		data_storage = config.data_storage()
		if data_storage == 'text':
			from . import data_text as data_module
		elif data_storage == 'sqlite':
			from . import data_sqlite as data_module
		else:
			print("data storage type {} doesn't exist".format(data_storage))
		best_guess = False
	except configparser.NoSectionError:
		best_guess = True
	except configparser.NoOptionError:
		best_guess = True

	if best_guess:
		if os.path.isfile(os.path.join(env, 'spyderweb.db')):
			from . import data_sqlite as data_module
		else:
			from . import data_text as data_module	

	data_module.env = env
	return(data_module)
	
	


# params
# fields: list of ticket fields to retrieve, if unspecified reads config
# filters: list of lists of [field, value, comparison]
# order: string, field to order by
# limit: int, how many items to retrieve
# ascending: bool, which way to order
#
# return
# list of dicts of ticket data
def get_ticket_data(fields = None, filters = 0, order='id', ascending = 1, limit = 0):
	active_data = set_data_storage()

	ticket_list = active_data.get_ticket_data(fields, \
	                                          filters, \
	                                          order, \
	                                          ascending, \
	                                          limit)
	return(ticket_list)


# Returns highest version number of ticket
def get_version(ticket_id):
	active_data = set_data_storage()
	ticket_version = active_data.get_version(ticket_id)
	return(ticket_version)


# Writes ticket data to storage
# 
# param:
# data, library of key:value pairs to store
# id, int ID of ticket to write
def set_ticket_data(ticket_id, data):
	active_data = set_data_storage()
	success = active_data.set_ticket_data(ticket_id, data)
	return(active_data)


# Creates new ticket
#
# param:
# data, library of key:value pairs for new ticket
#
# return: id
def create_ticket(data):
	active_data = set_data_storage()
	ticket_id = active_data.create_ticket(data)
	return(ticket_id)


# setup database
def initialize():
	active_data = set_data_storage()
	result = active_data.initialize()
	return(result)


def delete(ticket_id):
	active_data = set_data_storage()
	result = active_data.delete(ticket_id)
	return(result)

	
def hide(ticket_id):
	active_data = set_data_storage()
	result = active_data.hide(ticket_id)
	return(result)


def unhide(ticket_id):
	active_data = set_data_storage()
	result = active_data.unhide(ticket_id)
	return(result)


# update possible previous versions of the database
def upgrade():
	active_data = set_data_storage()
	result = active_data.upgrade()
	return(result)
