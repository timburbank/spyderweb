#!/bin/python

from lib import data


def list():
	fields = ['id', 'name', 'status']
	ticket_data = data.get_ticket_data(fields)
	list = ''
	for ticket in ticket_data:
		list = '{}{:<3}{:24}{}\n'.format(list, ticket['id'], ticket['name'], ticket['status'])
	print(list)
    
    
def view(id):
	fields = ['id', 'name', 'status', 'description']
	filters = {'id':id}
	ticket_data = data.get_ticket_data(fields, filters)
	
#	view = ticket_data
	underline = '==='
	for i in range(0,len(ticket_data[0]['name'])):
		underline = "{}=".format(underline)
	view = \
		'\n' \
		'{}  {} \n' \
		'{}\n' \
		'\n' \
		'{}\n\n' \
		'............................\n' \
		.format(ticket_data[0]['id'], ticket_data[0]['name'], underline, ticket_data[0]['description'])
		
	print(view)
    
def create():
	from lib import terminal
	name = terminal.input('name: ')
	description = terminal.input('description: ')
	print(name + "\n" + description)
    
def update(id):
	from lib import terminal
	
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

	# view(id) #use once we have actual storage
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
if __name__ == "__main__": # doesn't run if file is imported somewhere
	import sys
	
	if(len(sys.argv) > 1):
		arg = sys.argv[1] # get command line argument

		if arg == 'list':
			list()
		elif arg == 'view':
			view(sys.argv[2])
		elif arg == 'create':
			create()
		elif arg == 'update':
			update(sys.argv[2])
		elif arg == 'hide':
			hide()
		elif arg == 'delete':
			delete()
