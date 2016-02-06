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
	ticket_data = data.get_ticket_data(fields)
	
	view = \
		'{} {} \n' \
		'============== \n' \
		'\n' \
		'We are the crystal gems / We\'ll always save the day / ' \
		'And if you think we can\'t / We\'ll always find a way' \
		.format(ticket_data['id'], ticket_data['name'])
		
	print(view)
    
def create():
	print('create stub')
    
def update():
	print('update stub')
    
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
			update()
		elif arg == 'hide':
			hide()
		elif arg == 'delete':
			delete()
