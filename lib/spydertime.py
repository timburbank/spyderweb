# Time tracing tools
from . import data
import datetime
from datetime import datetime as datetime_ob

# Find if a ticket has a started timer
def find_started():
	ticket_data = data.get_ticket_data('')
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
	ticket_data = data.get_ticket_data('', [['id', ticket_id]])[0]
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
	ticket_data = data.get_ticket_data('', filters)
	
	try:
		prev_time_data = ticket_data[0]['time_log']
	except KeyError:
		prev_time_data = ''
		
	new_entry = 'START: {:%Y-%m-%d %H:%M:%S}' \
	            .format(datetime.datetime.now())
	time_data = '{}\n\n{}'.format(prev_time_data, new_entry)
	
	data.set_ticket_data(ticket_id, {'time_log': time_data})
	print('Starting time on ticket {}'.format(ticket_id))
	

def get_time(ticket_id = None):
	print('get_time({})'.format(ticket_id))