#!/bin/python

env = "env" # path or some reference to current environment directory
import os

from sys import version_info
py3 = version_info[0] > 2
if py3:
	import configparser
else:
	import ConfigParser as configparser 

from lib import data
from lib import config

# searche all fields until it finds one that matches the given key exactly
# and return the ID of that ticket
def search(search_key):
	fields = config.fields()
	
	for field in fields:
		filters = [[field, search_key]]
		try:
			ticket_data = data.get_ticket_data('', filters)[0]
			break
		except:
			pass
	return(ticket_data['id'])
		
	


def list(layout = 'default'):
	columns = config.list_fields(layout)
	filters = config.list_filters(layout)
	ticket_data = data.get_ticket_data(columns, filters)

	list = ''
	for ticket in ticket_data:
		row = ""
		for column in columns:
			#print(column)
			try:
				column_width = int(column[1])
			except:
				column_width = 0
			column_text = str(ticket[column[0]])
			if column_width is not 0:
				column_text = column_text[0:column_width - 1]
			row = '{prev}{name:<{width}}'.format(
			                                    prev=row, 
			                                    name=column_text,
			                                    width=column_width
			                                    )	
		#	print(column[0])
		#	print(ticket[column[0]])
		#	row = '{prev}{name:{width}}'.format(prev=row, name=ticket_data[0], width=ticket_data[1])
			
		print(row)
			

def show_ticket(id):
	
	fields = config.fields()
	fields.insert(0, 'id')
	
	ticket_version = data.get_version(id)
	filters = [['id', id]]
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
		prompt = '{}: '.format(field)
		prefill = config.field_default(field)
		ticket_data[field] = terminal.field_input(field, prompt, prefill)

	id = data.create_ticket(ticket_data)
	show_ticket(id)

	
def edit(id):
	from lib import terminal

	show_ticket(id)
	
	fields = config.fields()
	filters = [['id',id]]
	ticket_data = data.get_ticket_data(fields, filters)[0]

	print('Enter updated info, leave blank for unchanged')
	new_data = {}
	for field in fields:
		prompt = '{}: '.format(field)
		prefill = ticket_data[field]
		new_data[field] = terminal.field_input(field, prompt, prefill )
	data.set_ticket_data(id, new_data)
	show_ticket(id)

def remove(ticket_id, will_delete):
	
	if will_delete:
		from lib import terminal
		prompt = 'Are you sure you want to delete ticket {} (yes/no):'\
			.format(ticket_id)
		if terminal.input(prompt) == 'yes':
			data.delete(ticket_id)
			print('Ticket {} deleted'.format(ticket_id))
		else:
			print('Ok! Nevermind')
	else:
		data.hide(ticket_id)
		print('Ticket {} hidden. Restore with restore [id]'.format(ticket_id)) 

# initialize environment
def initialize():
	if not os.path.exists(env):
		os.makedirs(env)
	data.initialize()
	config.initialize()

def upgrade():
	data.upgrade()	
	
# handle command line inputs

# more graceful way? https://docs.python.org/2/library/argparse.html
if __name__ == "__main__": # doesn't run if file is imported somewhere
	import argparse
	parser = argparse.ArgumentParser()
	
	# -e can be set before or after the subcommand
	parser.add_argument('-e', '--environment')	

	subparsers = parser.add_subparsers(
		help = 'Commands', 
	    dest = 'command')
	# put all subparsers in a list for adding global arguments
	all_the_parsers = []	

	# Define available commands as subparsers
	list_p = subparsers.add_parser(
		'list', 
		help = 'List tickets')
	list_p.add_argument(
		'layout', 
	     default = 'default', 
	     nargs = '?', 
	     help = 'Display layout, set in config')
	all_the_parsers.append(list_p)

	view_p = subparsers.add_parser(
		'view', 
	    help = 'View info for a ticket')
	view_p.add_argument('param', help='Ticket ID')
	all_the_parsers.append(view_p)

	new_p = subparsers.add_parser(
		'new', 
		help = 'Create new ticket')
	all_the_parsers.append(new_p)

	edit_p = subparsers.add_parser(
		'edit',
		help = 'Edit ticket info')
	edit_p.add_argument('param', help = 'Ticket ID')
	all_the_parsers.append(edit_p)

	remove_p = subparsers.add_parser('remove', help = 'Remove ticket')
	remove_p.add_argument('param', help = 'Ticket ID')
	remove_p.add_argument(
		'-d', 
		'--delete', 
		action = 'store_true',
		help = 'Perminantly delete ticket, instead of hiding it')
	all_the_parsers.append(remove_p)
	
	init_p = subparsers.add_parser(
		'init', 
		help = 'Initialize project, creating database ' + \
		       'and default config file')
	all_the_parsers.append(init_p)

	upgrade_p = subparsers.add_parser(
		'upgrade', 
		help = 'Upgrades database if it was created for a previous ' + \
		       'incompatible version of Spyderweb')
	all_the_parsers.append(upgrade_p)
	
	time_p = subparsers.add_parser(
		'time', 
		help = 'Options for time tracking')
	time_p.add_argument('action', help = 'Time actions: start, stop, #')
	time_p.add_argument('param', help = 'Ticket ID', nargs = '?')
	all_the_parsers.append(time_p)

	# add global arguments	
	for some_parser in all_the_parsers:
		some_parser.add_argument('-e', '--environment')

	# set environment 
	args = parser.parse_args()
	
	if args.environment is not None:
		env = args.environment
	else:
		# set env to where script was run from 
		# automatically check for subdir 'env' or 'spyderweb'
		env_subdir = os.path.join(os.getcwd(), 'env')
		spyderweb_subdir = os.path.join(os.getcwd(), 'spyderweb')
		if os.path.exists(spyderweb_subdir):
			env = spyderweb_subdir
		elif os.path.exists(env_subdir):
			env = env_subdir
		else:
			env = os.getcwd()
	data.env = env	
	config.env = env

	# make sure we have a id for those that want it
	if hasattr(args, 'param'):
		try:
			ticket_id = int(args.param)
		except (ValueError, TypeError):
			try:
				ticket_id = search(args.param)
			except UnboundLocalError:
				pass
	
	# Execute the commands
	if args.command == 'list':
		try:
			list(args.layout)
		except configparser.NoSectionError:
			print('Layout "{}" not defined in config file' \
				  .format(args.layout))
			exit()
	
	elif args.command == 'view':
		show_ticket(ticket_id)
		
	elif args.command == 'new':
		create()
		
	elif args.command == 'edit':
		edit(ticket_id)
		
	elif args.command == 'remove':
		remove(ticket_id, args.delete)
	
	elif args.command == 'init':
		initialize()
		
	elif args.command == 'upgrade':
		upgrade()
		
	elif args.command == 'time':
		from lib import spydertime
		if args.action == 'start':
			spydertime.start_time(ticket_id)
		elif args.action == 'stop':
			spydertime.stop_time()
		else:
			spydertime.get_time(ticket_id)
	
	else:
		print('command not handled')
		exit()
	
	

