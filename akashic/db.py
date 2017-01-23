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

ensureDB()
