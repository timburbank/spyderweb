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

- fields (text, storing python library of field_name:value)

Versioning 

Edit ticket

1. create new field(s)

2. create new version, refering to the new fields and copying non-updated ones from the previous version
