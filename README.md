My "Operating System", a set of tools for viewing and editing data, mostly based
around the now-defunct rethinkDB.

If there's any tools in here that you'd like to use without the madness of my
trying to create an "operting system", submit a bug report and I'll see about
making it work stand alone. Or at least helping you do that work yourself.

Rethinkdb has an abstraction called "changefeeds" which lets you cheaply monitor a query for changes.

|item|decscription|status|
|----|------------|------|
|rq| use vim to edit rethinkdb tables| Works, you can only edit an entire table. No query support.|
|clusterize.py|Cluster your rethinkdb connections using ssh tunneling| WIP|
|ti| time tracker | Being rewritten|

