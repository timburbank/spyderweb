#!/bin/python

env = "environment_path" # path or some reference to current environment directory

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

	filters = {'id':id}
	ticket_data = data.get_ticket_data(fields, filters)[0]
	print("=========================")
	for field in fields:
		print("{}:\n  {}\n".format(field, ticket_data[field]))
	print("-------------------------")
    
def create():
	from lib import terminal
	name = terminal.input('name: ')
	description = terminal.input('description: ')
	
	ticket_data = {'name':name, 'description':description}
	data.create_ticket(ticket_data)
	print(name + "\n" + description)
    
def update(id):
	from lib import terminal

	show_ticket(id)
	
	fields = ['id', 'name', 'status', 'description']
	filters = {'id':id}
	ticket_data = data.get_ticket_data(fields, filters)

	print('Enter updated info, leave blank for unchanged')
	name = terminal.input('name: ')
	description = terminal.input('description: ')
	status = terminal.input('status: ')

	if len(name) == 0:
		name = ticket_data[0]['name']
	if len(description) == 0:
		description = ticket_data[0]['description']
	if len(status) == 0:
		status = ticket_data[0]['status']

	# show_ticket(id) #use once we have actual storage
	underline = '==='
	for i in range(0,len(name)):
		underline = "{}=".format(underline)
	view = \
		'\n' \
		'{}  {} \n' \
		'{}\n' \
		'\n' \
		'{}\n\n' \
		'............................\n' \
		.format(ticket_data[0]['id'], name, underline, description) 
	print(view)


def hide():
	print('hide stub')

def delete():
	print('delete stub')



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
		elif arg == 'update':
			update(sys.argv[2])
		elif arg == 'hide':
			hide()
		elif arg == 'delete':
			delete()
