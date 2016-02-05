Design Principals
=================

Self contained, and runs without any installation 

Data portability. Integrates with other project management systems

Async updating - display what we know and change display if different information is recieved (for one way sync this isn't really necessary)


What is the actual purpose of this tool?
- To give me a consistent workflow, while letting my projects be shared in the manner that's most effective for them

Problem: Github works well for Git and for public projets. Trac works well for mercurial and private projects. Phabricator works well for repository hosting but is a weird ecosystem to work in. I also want to be able to archive my data and store it with the project.

All this tool really needs to do is keep track of a bunch of tickets, and update remote sources to match. *It's a sharing tool, not a collaboration tool*

- Build as CLI first
- Update from repository*
- Export to other services
- Add web interface 



*Most effective way to sync is probably through bash interface <http://www.bogotobogo.com/python/python_subprocess_module.php>
