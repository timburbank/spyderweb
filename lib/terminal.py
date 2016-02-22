# Functions for dealing with terminal interaction

def input(prompt):
	from sys import version_info
	py3 = version_info[0] > 2
	if py3:
		content = input(prompt)
	else:
		content = raw_input(prompt)
	return(content)

def long_input(prompt):
	# from http://stackoverflow.com/q/10129214
	import os, subprocess, tempfile

	(fd, path) = tempfile.mkstemp()
	fp = os.fdopen(fd, 'w')
	fp.write('# {}'.format(prompt))
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
	return(content)

