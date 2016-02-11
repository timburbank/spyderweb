#!/bin/python

env = "env" # path or some reference to current environment directory

from lib import data
data.env = env
from lib import config
config.env = env


def list():
	fields = config.list_fields()
	ticket_data = data.get_ticket_data(fields)

	list = ''
	for ticket in ticket_data:
		list = '{}{:<3}{:24}{}\n'.format(list, \
			ticket[fields[0]], \
			ticket[fields[1]], \
			ticket[fields[2]])
			
	print(list)


def show_ticket(id):
	fields = config.fields()
	fields.insert(0, 'id')

	filters = {'id':id}
	ticket_data = data.get_ticket_data(fields, filters)[0]
	print("=========================")
	for field in fields:
		print("{}:\n  {}\n".format(field, ticket_data[field]))
	print("-------------------------")

def create():
	from lib import terminal
	fields = config.fields()
	ticket_data = {}
	# TODO allow defaults?
	# might be helpful http://stackoverflow.com/a/1602964
	for field in fields:
		ticket_data[field] = terminal.input('{}: '.format(field))

	id = data.create_ticket(ticket_data)

	# show_ticket(id)
	fields.insert(0, 'id')
	ticket_data['id'] = id
	print("=========================")
	for field in fields:
		print("{}:\n  {}\n".format(field, ticket_data[field]))
	print("-------------------------")

def edit(id):
	from lib import terminal

	show_ticket(id)
	
	fields = config.fields()
	filters = {'id':id}
	ticket_data = data.get_ticket_data(fields, filters)[0]

	print('Enter updated info, leave blank for unchanged')
	new_data = {}
	for field in fields:
		new_data[field] = terminal.input('{}: '.format(field))
		if len(new_data[field]) == 0:
			new_data[field] = ticket_data[field]

	print("=========================")
	for field in fields:
		print("{}:\n  {}\n".format(field, new_data[field]))
	print("-------------------------")


def hide():
	print('hide stub')

def delete():
	print('delete stub')

# initialize environment
def initialize():
	data.initialize()

# handle command line inputs

# more graceful way? https://docs.python.org/2/library/argparse.html
if __name__ == "__main__": # doesn't run if file is imported somewhere
	import sys
	
	if(len(sys.argv) > 1):
		arg = sys.argv[1] # get command line argument

		if arg == 'list':
			list()
		elif arg == 'view':
			show_ticket(sys.argv[2])
		elif arg == 'create':
			create()
		elif arg == 'edit':
			edit(sys.argv[2])
		elif arg == 'hide':
			hide()
		elif arg == 'delete':
			delete()
		elif arg == 'init':
			initialize()
