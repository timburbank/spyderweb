from lib import db


def list():
	data = db.get('ticket')
	for item in data:
		print(item)
	
	list =  \
		'number  name                status \n' \
    		'1       first ticket        new \n' \
		'2       second ticket       closed \n' \
		'3       third ticket        kinda workable \n' \
    
    
def view():
	
	view = \
		'#1 Ticket Name \n' \
		'============== \n' \
		'\n' \
		'We are the crystal gems / We\'ll always save the day / ' \
		'And if you think we can\'t / We\'ll always find a way' 
		
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
	arg = sys.argv[1] # get command line argument

	if arg == 'list':
		list()
	elif arg == 'view':
		view()
	elif arg == 'create':
		create()
	elif arg == 'update':
		update()
	elif arg == 'hide':
		hide()
	elif arg == 'delete':
		delete()
