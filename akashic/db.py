import rethinkdb as r


mainDB = 'akashic'

tables = {
    'dns':{},
    'logs':{},
    'alerts':{},
    'files':{},
    'cache':{},
}

indexes = {
    'dns': ['name'],
    'cache': ['name'],
    'files': ['name',],
    'logs': ['tags'],
    'alerts': ['ctime'],
}

multiIndexes = {
    'files': ['tags',],
}

r.db('akashic').table('files').index_create("tags", multi=True)

def ensureDB():
    r.connect().repl()
    dbs = r.db_list().run()
    if not mainDB in r.db_list().run():
        print(r.db_create(mainDB).run())
    r.connect(db=mainDB).repl()

    existingdbs=r.table_list().run()
    for key, value in tables.items():
        if not key in existingdbs:
            print(r.table_create(key,**value).run())
        if key in indexes:
            newindexes =  [index for index in indexes[key] if index not in  r.table(key).index_list().run()]
            for index in newindexes:
                r.table(key).index_create(index).run()
#ensureDB()
import os
from collections import ChainMap

localDefaults={
'akashic_db':'akashic',
'akashic_user':'admin',
'akashic_port':'28015',
'akashic_password':'',
'akashic_host':'localhost',
}

defaultSettings=ChainMap(os.environ, localDefaults)

def addConnToParser(parser):
    """
    Takes a parser objects, adds options for connectiong,
    Connects.
    Returns a query object. In the future that may change.
    """
    parser.add_argument('--db', type=str,
                    help='Which db to edit', default=defaultSettings['akashic_db'])
    parser.add_argument('--user', type=str,
                    help='Which user to log in as', default=defaultSettings['akashic_user'])
    parser.add_argument('--port', type=str,
                    help="The port of your rethinkDB server",
                    default=defaultSettings['akashic_port'])
    parser.add_argument('--password', type=str,
                    default=defaultSettings['akashic_password'])
    parser.add_argument('--host', type=str,
                    help='The address of you rethinkDB server', default=defaultSettings['akashic_host'])

def connectFromArgs(args):
    connectionArgs = {k:v for k,v in vars(args).items() if k in ('db','user','port','password','host')}
    return r.connect(**connectionArgs)
