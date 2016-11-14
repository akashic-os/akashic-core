A tool for viewing/graphing data stored in rethinkdb.

Like good unix tools, we'd really like it if our text streams could be edited.

Text streams created by these tools will start with #akashic-json {json full of metadata about the query, and how to save changes}.
By default the only metadata we'll include is the database and table.

We hope this will work alright with tools like [jq](https://robots.thoughtbot.com/jq-is-sed-for-json)
