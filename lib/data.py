# Functions for interacting with the database

# Confirm we're in the right file
def database():
	print('Date a Bass?')

# params
# fields: list of ticket fields to retriev
# filters: dictionary of field:value:comparison
# order: string, field to order by
# limit: int, how many items to retrieve
# ascending: bool, which way to order
def get_ticket_data(fields, filters = 0, order='id', ascending = 1, limit = 0):

	temp_data_set = [ \
		{'id':1, 'name':'Garnet', 	'description':'We are the crystal gems',	'status':'todo'}, \
		{'id':2, 'name':'Amethyst', 'description':"We'll always save the day",	'status':'complete'}, \
		{'id':3, 'name':'Pearl', 	'description':"And if you think we can't",	'status':'workable'}, \
		{'id':4, 'name':'Stephen', 	'description':"We'll always find a way",	'status':'todo'} \
	]
	
	data = []
	for item in temp_data_set:
		datum = {}
		pass_filters = True	
		if(filters != 0):
			for key, value in filters.items():
				if (int(item[key]) == int(value)):
					pass_filters = True
				else:
					pass_filters = False
		if(pass_filters):
			for field in fields:
				datum[field] = item[field]
			data.append(datum)
		
		# need to implement filters
		
	return(data)
	
