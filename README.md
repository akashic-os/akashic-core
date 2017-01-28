My "Operating System", a set of tools for viewing and editing data, mostly based
around rethinkDB (the company behind which went out of business, but I think the
db will still get some love).

Install with

    git clone https://github.com/akashic-os/akashic-core.git
    cd akashic-core
    python3 setup.py develop --user

Not a kernel, or an actual OS. An OS in the same way gnu is an OS, or a web
browser is an OS.

There are a lot of problems in computing that get a lot easier when you have one
unified view of your data. This aims to build something on top of the unified
view offered by rethinkdb.

If there's any tools in here that you'd like to use without the madness of my
trying to create an "operting system", submit a bug report and I'll see about
making it work stand alone. Or at least helping you do that work yourself.

Rethinkdb has an abstraction called "changefeeds" which lets you cheaply monitor a query for changes.

#Todo

##Tools

 - [X] rq, edit your data using vim and yaml. Very basic query support
  - [] Make rethinkdb support DeepDiff diffs so that we can edit objects with
    binary data in them.
  - [] Make use of yaml tags for transforming data (humanizing dates, on both
    input and output).

 - [] afs, a tagged filesystem implemenation for rethinkdb
  - [] get basic implementation up and running
  - [] add some test cases (fusepy should make this real easy, but it does't)

 - [] Extend pythons logging to support data objects

 - [] Add an RPC layer (maybe based on hug?)

##Daemons

 - [] dbus notification support for "alerts" table
 - [] generate notifications from query

 - [] Add metadata to image files
 - [] Add metadata to movie files
 - [] Add metadata to audio files
 - [] Thumbnail stuff

 - [] caldav/carddav server for synchronizing contacts and the like

#Android-native

 - [] get rethinkdb running an android at all
 - [] notification support for "alerts" table
 - [] contact synchronization
 - [] share file on afs
