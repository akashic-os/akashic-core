My "Operating System", a set of tools for viewing and editing data, mostly based
around rethinkDB (the company behind which went out of business, but I think the
db will still get some love).

Not a kernel, or an actual OS. An OS in the same way gnu is an OS, or a web
browser is an OS.

There are a lot of problems in computing that get a lot easier when you have one
unified view of your data. This aims to build something on top of the unified
view offered by rethinkdb.

If there's any tools in here that you'd like to use without the madness of my
trying to create an "operting system", submit a bug report and I'll see about
making it work stand alone. Or at least helping you do that work yourself.

Rethinkdb has an abstraction called "changefeeds" which lets you cheaply monitor a query for changes.

|item|decscription|status|
|----|------------|------|
|rq| use vim to edit rethinkdb tables| Works, you can only edit an entire table. No query support.|
|clusterize.py|Cluster your rethinkdb connections using ssh tunneling,
optionally generate cjdns config for unified IP namespace that works over lan| WIP|
|ti| time tracker | Being rewritten|
|afs|A tag-based FUSE filesystem backed by rethinkdb | WIP |
