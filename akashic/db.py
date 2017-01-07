import rethinkdb as r

mainDB = 'akashic'

tables = {
    'dns':{},
    'logs':{},
    'alerts':{},
}

indexes = {
    'dns': ['name'],
    'logs': ['tags'],
    'alerts': ['ctime'],
}


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
