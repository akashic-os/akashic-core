A tool for viewing/filtering/etc data stored in rethinkdb.


# Creating a new command

We use click, because it seems to have some pretty decent tab completion, and it's not a bad way to define new commands.

It does make some things akward though, like inheretence. To define you own command, and include the standard "connection" code, do

```python

from akashic.connection import connect, connectionDecorators, composed

@click.command()
@composed(*connectionDecorators)
def cli(**kwargs):
    r = connect(**kwargs)
cli()


```

"r" will be a connection to the rethinkdb DB specified, that you can then do your real actions to.
A bit of a pain, but not too bad.

# Piping Data

How we might go about this, nothing is implemented that uses it.

Like good unix tools, we'd really like it if our text streams could be edited.

Text streams created by these tools will start with #akashic-json {json full of metadata about the query, and how to save changes}.
By default the only metadata we'll include is the database and table.

We hope this will work alright with tools like [jq](https://robots.thoughtbot.com/jq-is-sed-for-json)
