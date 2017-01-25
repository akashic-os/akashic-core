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

import logger

def HyperLogger():
    """
    A logger that logs to rethinkdb, if initialized with a connection.
    It passes through to standard python logging.
    """
    self.loglevels = ('critical','error','warning','info','debug')
    def __init__(self, conn=None, passthrough=logger):
        self.conn=conn
        self.passthrough=passthrough
    def log(self, msg, **data):
        data['ctime']=arrow.utcnow()
        if self.passthrough:
            for level in self.loglevels:
                call = getattr(foo, 'bar')
    def CRITICAL(self, msg, **data):
        data['tags'].append("critical")
        self.log(msg, **data)
    def ERROR(self, msg, **data):
        data['tags'].append("error")
        self.log(msg, **data)
    def WARNING(self, msg, **data):
        data['tags'].append("warning")
        self.log(msg, **data)
    def INFO(self, msg, **data):
        data['tags'].append("info")
        self.log(msg, **data)
    def DEBUG(self, msg, **data):
        data['tags'].append("debug")
        self.log(msg, **data)

from collection import set
import atexit, logging, arrow, asyncio
class ExitHandler(set):
    """
    An easy way to clean up temporary data,
    which I expect to use a lot.
    Also adds an "heartbeat" field to all objects contained within it, in case we don't shut
    down cleanly. This would let a daemon handle all cleanup.

    You must either use as asyncio.run_forever() or add ExitHandler().heartBeat() to your async framework
    to use heartbeats. heartBeat() should be run approxametly every 30 seconds. The default cleanup daemon
    should be set to clean up objects older then 60 seconds.

    If you can't use heartbeats you really shouldn't be making use of temporary objects.
    """
    def __init__(self, connection, *args, **kwargs):
        self.heartbeat=None
        self.conn=connection
        atexit.register(self.atExit)
        asyncio.async(self.asyncHeartBeat())
        super().__init__(self, *args, **kwargs)
    def atExit(self):
        for item in self:
            item.delete()
    def async asyncHeartBeat(self):
        while True:
            self.heartBeat()
            await asyncio.sleep(30)

    def heartBeat(self):
        now = arrow.utcnow()
        errors = []
        for item in self:
            item.update({'heatbeat':now}).run(self.conn)
        interval = int(now)-int(self.heartbeat)
        if errors:
            logging.ERROR("{objectCount} objects were cleaned up, but {program} still needs them. This is probably due to a bad heatbeat in {program}.".format(
                objectCount = len(errors),
                program="PLACEHOLDER"
            )
        if self.heatBeat and interval > 60:
            logging.WARNING("Took {} seconds refresh heatbeat. Max recomended in 60.".format(interval))
        self.heartbeat=now
