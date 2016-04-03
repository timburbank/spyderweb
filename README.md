Spyderweb
=========

Spyderweb is an issue tracker or project management tool, that runs locally through a command line interface. It's intended for small, usually single person, projects where a full web based bug tracker would be unnecessary and cumbersome.

Installing and Running
----------------------

Git clone or download the files.

Spyderweb can be run simply by calling `python spyderweb.py [command]`. The easiest way to use it is by creating a bash alias, by adding something like `alias spy="python /path/to/spyderweb/spyderweb.py"` to `~/.bashrc` or `~/.bash_profile`(on OSX it needs to be `~/.bash_profile`)

To setup a project, navigate to the directory you want to keep your Spyderweb environment in, and enter `spy init`. This will create `spyderweb.db` were the data is stored, and `spyderweb.ini` where you can configure the current project.

Note: when you run any Spyderweb command in a directory, it will automatically check for a `spyderweb/` or `env/` subdirectory, so it can be convenient to initialize your Spyderweb environment in one of these directories.


Commands
--------

- `init` Initializes Spyderweb environment in the current directory
- `list [LAYOUT]` List tickets. `[LAYOUT]` (optional) specifies a layout defined in `spyderweb.ini`
- `view {TICKET_ID}` Display ticket with given ticket ID
- `new` Create ticket.
- `edit {TICKET_ID}` Edits ticket with given ticket ID
- `remove [-d, --delete] {TICKET_ID}` Removes ticket with given ticket ID. If `-d` flag is given, all ticket data will be delete from the database. If not the ticket is simply hidden, and maybe someday if there's a `restore` command it can be brought back.
- `upgrade` Upgrades Spyderweb environment. Only needed if changes to the code base have broken an existing environment.
