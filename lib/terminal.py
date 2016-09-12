# Functions for dealing with terminal interaction

import sys

# taken from https://www.metachris.com/2015/11/python-tools-for-string-unicode-encoding-decoding-printing/
def out(text):
    # Prints a (unicode) string to the console, encoded depending on the stdout
    # encoding (eg. cp437 on Windows). Works with Python 2 and 3.
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        bytes_string = text.encode(sys.stdout.encoding, 'backslashreplace')
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write(bytes_string)
        else:
            text = bytes_string.decode(sys.stdout.encoding, 'strict')
            sys.stdout.write(text)
    sys.stdout.write("\n")

def short_input(prompt='', prefill=''):
	from sys import version_info

	print(prefill)
	py3 = version_info[0] > 2
	if py3:
		user_input = input(prompt)
	else:
		user_input = raw_input(prompt)
	
	if user_input == '':
		content = prefill
	else:
		content = user_input
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

	# If subprocess returns non-zero try a different editor
	editor = os.getenv('EDITOR', 'vim')
	if subprocess.call('%s %s' % (editor, path), shell=True):
		editor = os.getenv('EDITOR', 'vi')
		if subprocess.call('%s %s' % (editor, path), shell=True):
			editor = os.getenv('EDITOR', 'notepad')
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
		input_type = config.field_type(field)
	except:
		input_type = 'text'
	if input_type == 'text':
		field_input = short_input(prompt, prefill)
	elif input_type == 'long_text':
		field_input = long_input(prompt, prefill)
	else:
		# TODO throw exception here
		print("Unrecognized input type in config")
	return(field_input)
