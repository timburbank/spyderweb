#!/bin/python

env = "env" # path or some reference to current environment directory
import os
#env = os.getcwd() set env to where script was run from 

from lib import data
#data.env = env
from lib import config
#config.env = env


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

	ticket_version = data.get_version(id)
	filters = {'id':id}
	ticket_data = data.get_ticket_data(fields, filters)[0]
	print("=========================")
	print("version: {}".format(ticket_version))
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
		# TODO set which to use in config
		if field == "description":
			ticket_data[field] = terminal.long_input('# {}: '.format(field))
		else:
			ticket_data[field] = terminal.input('{}: '.format(field))

	id = data.create_ticket(ticket_data)
	show_ticket(id)

	
def edit(id):
	from lib import terminal

	show_ticket(id)
	
	fields = config.fields()
	filters = {'id':id}
	ticket_data = data.get_ticket_data(fields, filters)[0]

	print('Enter updated info, leave blank for unchanged')
	new_data = {}
	for field in fields:
		if field == "description":
			new_data[field] = terminal.long_input(ticket_data[field])
		else:
			new_data[field] = terminal.input('{}: '.format(field))
	
	data.set_ticket_data(id, new_data)
	show_ticket(id)

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
	import argparse
	parser = argparse.ArgumentParser()
	
	

	subparsers = parser.add_subparsers()
	# put all subparsers in a list for adding global arguments
	all_the_parsers = []	

	# Define available commands as subparsers
	list_p = subparsers.add_parser('list')
	list_p.set_defaults(func=list)
	all_the_parsers.append(list_p)

	view_p = subparsers.add_parser('view')
	view_p.add_argument('param')
	view_p.set_defaults(func=show_ticket)
	all_the_parsers.append(view_p)

	new_p = subparsers.add_parser('new')
	new_p.set_defaults(func=create)
	all_the_parsers.append(new_p)

	edit_p = subparsers.add_parser('edit')
	edit_p.add_argument('param')
	edit_p.set_defaults(func=edit)
	all_the_parsers.append(edit_p)

	hide_p = subparsers.add_parser('hide')
	hide_p.add_argument('param')
	hide_p.set_defaults(func=hide)
	all_the_parsers.append(hide_p)	

	delete_p = subparsers.add_parser('delete')
	delete_p.add_argument('param')
	delete_p.set_defaults(func=delete)
	all_the_parsers.append(delete_p)
	
	init_p = subparsers.add_parser('init')
	init_p.set_defaults(func=initialize)
	all_the_parsers.append(init_p)

	# add global arguments	
	for some_parser in all_the_parsers:
		some_parser.add_argument('-e', '--environment')

	# set environment 
	args = parser.parse_args()
	if args.environment is not None:
		env = args.environment
	else:
		# set env to where script was run from 	
		env = os.path.join(os.getcwd(), 'env')

	data.env = env	
	config.env = env

	# Execute the commands (can have one possitional argument 'param')
	try:
		param = getattr(args, 'param')
		args.func(param)
	except:
		args.func()
	

