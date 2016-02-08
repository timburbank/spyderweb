# Functions for dealing with terminal interaction

def input(prompt):
	from sys import version_info
	py3 = version_info[0] > 2
	if py3:
		name = input(prompt)
	else:
		name = raw_input(prompt)
	return(name)
