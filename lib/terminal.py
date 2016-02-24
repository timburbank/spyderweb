# Functions for dealing with terminal interaction

def input(prompt='', prefill=''):
	from sys import version_info

	print(prefill)
	py3 = version_info[0] > 2
	if py3:
		content = input(prompt)
	else:
		content = raw_input(prompt)
	return(content)

def long_input(prompt='', prefill=''):
	# from http://stackoverflow.com/q/10129214
	import os, subprocess, tempfile
	
	# add #s to each line of prompt so we can remove them later
	prompt_lines = prompt.split("\n")
	prefixed_prompt = ''
	for line in prompt_lines:
		prefixed_prompt = "{}# {}\n".format(prefixed_prompt, line)

	(fd, path) = tempfile.mkstemp()
	fp = os.fdopen(fd, 'w')
	fp.write("{}\n{}".format(prefixed_prompt, prefill))
	fp.close()

	editor = os.getenv('EDITOR', 'vi')
	#print(editor, path)
	subprocess.call('%s %s' % (editor, path), shell=True)

	# read contents and remove lines with "#"
	content = ""
	with open(path, 'r') as f:
		for line in f:
			stripped_line = line.strip()
			if not stripped_line.startswith("#"):
				content = "{}{}".format(content, line)
	
	os.unlink(path)
	stripped_content = content.strip()
	# return blank string if unchanged (should maybe be None instead?)
	if stripped_content == prefill.strip():
		stripped_content = ""
	return(stripped_content)

# gets input in the proper manner for the given field
def field_input(field, prompt='', prefill=''):
	from lib import config
	try:
		input_type = config.get_value_list('field_input_types', field)[0]
	except:
		input_type = 'text'
	if input_type == 'text':
		field_input = input(prompt, prefill)
	elif input_type == 'long_text':
		field_input = long_input(prompt, prefill)
	else:
		# TODO throw exception here
		print("Unrecognized input type in config")
	return(field_input)
		
#print(long_input("file test"))

