ticket database setup

=====================

Tickets are a set of key:value pairs

tickets ?? 

----------

- id

- timestamp

We only need this table if selecting unique IDs from the fields table is too expensive ...we should probably have this table

fields

-------------

- id

- timestamp

- ticket_id

- name

- content

- type? (can probably just check from config)

- version?

versions

--------

- id

- timestamp

- ticket_id

- version_number

- fields (text, comma separated field IDs)

Versioning 

I think it's actually better just to store the version in each ticket field. 

Edit ticket:
1. Determine new version number
2. Add new fields with that version number.
3. When selecting ticket, loop over list of fields from config and query for the one with the highest version number (version numbers won't necessarily be the same if only a few fields are edited - the 'ticket verison' is determined by the highest version number in a field)

Edit ticket (prev)

1. create new field(s)

2. create new version, refering to the new fields and copying non-updated ones from the previous version
