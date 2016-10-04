#!/bin/python

env = "env" # path or some reference to current environment directory
import os

from sys import version_info
import sys

py3 = version_info[0] > 2
if py3:
	import configparser
else:
	import ConfigParser as configparser 

from lib import data
from lib import config
from lib import terminal

# searche all fields until it finds one that matches the given key exactly
# and return the ID of that ticket
def search(search_key):
	fields = config.fields()
	
	for field in fields:
		filters = [[field, search_key]]
		try:
			ticket_data = data.get_ticket_data(None, filters)[0]
			break
		except:
			pass
	return(ticket_data['id'])
		
	


def list(layout = 'default'):
	columns = config.list_fields(layout)
	filters = config.list_filters(layout)
	ticket_data = data.get_ticket_data(None, filters)

	list = ''
	for ticket in ticket_data:
		row = ""
		for column in columns:
			try:
				column_width = int(column[1])
			except:
				column_width = 0
			column_text = str(ticket[column[0]]).replace('\n', ' ').replace('\r', '')
			if column_width is not 0:
				column_text = column_text[0:column_width - 1]
			row = '{prev}{name:<{width}}'.format(
			                                    prev=row, 
			                                    name=column_text,
			                                    width=column_width
			                                    )	
		
		# color holds available colors as array or object
		# config.list_color(color) returns (field, value) tuple
		# for color in colors
		# if list_color(color)[1] = ticket[list_color]:
		# 	row = colors.color + row + colors.end
		
		terminal.out(row)
			

def show_ticket(id):
	
	fields = config.fields()
	
	ticket_version = data.get_version(id)
	filters = [['id', id]]
	ticket_data, = data.get_ticket_data(fields, filters)
	terminal.out("=========================")
	terminal.out("version: {}".format(ticket_version))
	terminal.out('id: {}'.format(ticket_data['id']))
	for field in fields:
		terminal.out("{}:\n  {}\n".format(field, ticket_data[field]))
	terminal.out("-------------------------")

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

	ticket_id = data.create_ticket(ticket_data)
	show_ticket(ticket_id)

	
def edit(id, field = None):

	show_ticket(id)
	
	if field is None:
		fields = config.fields()
	else:
		fields = [field]

	filters = [['id',id]]
	ticket_data = data.get_ticket_data(fields, filters)[0]

	terminal.out('Enter updated info, leave blank for unchanged')
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
			terminal.out('Ticket {} deleted'.format(ticket_id))
		else:
			terminal.out('Ok! Nevermind')
	else:
		data.hide(ticket_id)
		terminal.out('Ticket {} hidden. Restore with restore [id]'.format(ticket_id)) 

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
	edit_p.add_argument(
		'-f',
		'--field',
		nargs = '?',
		help = 'Edit only the specified field')
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
	time_p.add_argument('-D', '--days', help = 'Time range in days past')
	time_p.add_argument('-d', '--date', help = 'Show time on certain date')
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
			terminal.out('Layout "{}" not defined in config file' \
				  .format(args.layout))
			exit()
	
	elif args.command == 'view':
		show_ticket(ticket_id)
		
	elif args.command == 'new':
		create()
		
	elif args.command == 'edit':
		edit(ticket_id, args.field)
		
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
		elif args.action == 'show':
			# currently no ticket + time limit version
			try:
				spydertime.show_time(ticket_id)
			except NameError:
				from datetime import datetime as datetime_ob, timedelta
				import datetime

				if args.days is not None:
					max_time = datetime.datetime.now()
					min_time = max_time - timedelta(days = int(args.days))
					spydertime.show_time(min_time = min_time, 
					                     max_time = max_time)
				
				elif args.date is not None:
					date = datetime_ob.strptime(args.date, '%Y-%m-%d')
					spydertime.show_time(min_time = date, 
					                     max_time = date)	
				
				else:
					spydertime.show_time()
	
	else:
		terminal.out('command not handled')
		exit()
	
	

