# Time tracing tools
from . import data
from . import config
import datetime
from datetime import datetime as datetime_ob, timedelta

# Find if a ticket has a started timer
def find_started():
	ticket_data = data.get_ticket_data(None)
	started = None
	for ticket in ticket_data:
		try:
			last_line = ticket['time_log'].split('\n')[-1]
			if last_line.startswith('START'):
				started = ticket['id']
				break
		except:
			pass
	return(started)		
	
	
def stop_time():
	try:
		ticket_id = int(find_started())
	except TypeError:
		print('No ticket started')
		exit()
	ticket_data = data.get_ticket_data(None, [['id', ticket_id]])[0]
	existing_time_data = ticket_data['time_log']
	start_string = existing_time_data.strip()[-19:]
	
	start_time = datetime_ob.strptime( start_string, '%Y-%m-%d %H:%M:%S')
	stop_time = datetime.datetime.now()
	
	# get rid of the microseconds on elapsed time
	elapsed_time = str(stop_time - start_time).split('.')[0]
	
	time_data = '{}\nEND: {:%Y-%m-%d %H:%M:%S}\nDURATION: {}'.format(
		existing_time_data,
		stop_time,
		elapsed_time
	)
	
	data.set_ticket_data(ticket_id, {'time_log': time_data})
	
	print(
		'Stopping time on ticket {}, {} elapsed'.format(
		ticket_id, 
		elapsed_time))


def start_time(ticket_id):
	
	if find_started() is not None:
		stop_time()
	
	filters = [['id', ticket_id]]
	ticket_data = data.get_ticket_data(None, filters)
	
	try:
		prev_time_data = ticket_data[0]['time_log']
	except KeyError:
		prev_time_data = ''
		
	new_entry = 'START: {:%Y-%m-%d %H:%M:%S}' \
	            .format(datetime.datetime.now())
	time_data = '{}\n\n{}'.format(prev_time_data, new_entry)
	
	data.set_ticket_data(ticket_id, {'time_log': time_data})
	print('Starting time on ticket {}'.format(ticket_id))
	
# Get time for a single ticket, limited by option date ranges
# Params:
# ticket_id, ID of ticket to get time for
# min_time, datetime to ignore everything before
# max_time, datetime to ignore everything after
def get_ticket_time(ticket_id, min_time = None, max_time = None):
	import re
	duration_regex = re.compile(r'\d+:\d\d:\d\d')
	date_regex = re.compile(r'\d\d\d\d-\d\d-\d\d')

	# get tim_log field
	ticket_data = data.get_ticket_data(['time_log'], [['id', ticket_id]])
	time_log = ticket_data[0]['time_log']
	lines = time_log.splitlines()

	# to be a valid date entry, we need a START line, followed by an END
	# line, followed by a DURATION line. There can be other stuff between them	
	search_status = ''
	total_delta = timedelta()

	for line in lines:
		if line.startswith('START'):
			search_status = 'start'
		elif line.startswith('END') and search_status is 'start':
			search_status = 'end'
			end_mo = date_regex.search(line)
		elif line.startswith('DURATION') and search_status is 'end':
			dur_mo = duration_regex.search(line)
			try:
				end_date = datetime_ob.strptime( \
					end_mo.group(), \
					'%Y-%m-%d')

				if max_time is None \
						or (end_date >= min_time \
						and end_date <= max_time):

					# TODO: handle durations greater than one day
					logged_time = datetime_ob.strptime(dur_mo.group(), \
					                                   '%H:%M:%S')
					logged_delta = timedelta(hours = logged_time.hour, 
					                         minutes=logged_time.minute, 
					                         seconds=logged_time.second)
					total_delta += logged_delta


			except AttributeError:
				print('Duration in ticket {} unrecognized'.format(ticket_id))
	return(total_delta)




	print('get_ticket_time({})'.format(ticket_id))
	return 1


def show_time(ticket_id = None, min_time = None, max_time = None):
	# an awkward amount of this is just so that we can show 
	# a ticket field's content in the list of times
	if ticket_id is not None:
		total_time = get_ticket_time(ticket_id)
	else:
		try:
			list_field = config.time_list_field()
			columns = [list_field]
		except:
			list_field = None
			columns = []

		total_time = timedelta()
		ticket_data = data.get_ticket_data(columns)

		list_field_width = 0
		for field in config.list_fields():
			if field[0] == list_field:
				list_field_width = field[1]

		for ticket in ticket_data:
			ticket_time = get_ticket_time(ticket['id'], min_time, max_time)
			if list_field is not None:
				list_text = ticket[list_field]
			else: 
				list_text = ''
			print('{id} {field:<{width}} {time}'.format( \
				id = ticket['id'], \
				field = list_text, \
			    time = ticket_time, \
			    width = list_field_width))
			total_time += ticket_time
	print('----')
	print(total_time)