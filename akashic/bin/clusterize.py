#!/usr/bin/env python3
# encoding: utf-8

"""
Record this computers public and private IP.

Check to see what CJDNS routes work

Set up tunnels to the rethinkdb instances on remote machines

Push data about yourself into the rethinkdb cluster

Synchronize databases

loop
    See which tunnels have changed

    Rebuild cjdns config files

    rebuild hosts file

---

It must be restarted whenever you reconnect to the internet.

"""
import socket, requests, time, asyncio, sh
from json import loads
from collections import ChainMap

def jsonip():
    return loads(requests.get('http://jsonip.com').text)['ip']
def ippl():
    return requests.get('http://ip.42.pl/raw').text
def httpbin():
    return loads(requests.get('http://httpbin.org/ip').text)['origin']

ipfuncs = [jsonip,ippl,httpbin]
ip = None

for f in ipfuncs:
    try:
        ip = f()
        break
    except:
        print('failed to get ip with'+str(f))

hostname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
lanip = s.getsockname()[0]
s.close()

default = {
    'name':None,
    'lan':None,
    'internet':None,
    'cjdns':None,
    'edgeNode':False,
}

me = {
    'name': hostname,
    'lan':lanip,
    'internet':ip,
}

import rethinkdb as r
r.connect(db='akashic').repl()


remoteMe = r.table('dns').get_all(me['name'], index='name').run()
remoteMe = [i for i in remoteMe]

if len(remoteMe) > 1:
    for i in remoteMe[1:]:
        r.table("dns").get(i['id']).delete().run()

if not remoteMe:
    newMe = ChainMap(me,default)
    r.table('dns').insert(me).run()
    remoteMe = r.table('dns').get_all(me['name'], index='name').run()
    remoteMe = [i for i in remoteMe]
elif remoteMe:
    newMe = ChainMap(me, remoteMe, default)
    r.table('dns').replace(newMe).run()

remoteMe=remoteMe[0]

from multiprocessing import Process, Queue
def dnsFeed(q):
    #feed = r.table('dns').changes(include_initial=True).filter(lambda record:
    #    record["name"] == me['name']).run()
    feed = r.table('dns').changes(include_initial=True).run()
    for change in feed:
        q.put(change)

connections = {}

q = Queue()
p = Process(target=dnsFeed, args=(q,))
p.start()

tunnelPort = 23300 #Seems like an alright block.
def sshTunnel(change):
    global tunnelPort
    name = change['new_val']['name']
    tryOrder = ['cjdns','lan','internet']
    if name in connections:
        port = connections[name]['port']
        del connections[name]
    else:
        port = tunnelPort
        tunnelPort = tunnelPort+1
    for i in tryOrder:
        try:
            pass
#            p = sh.ssh(['-L','{local_port}:localhost:{remote_port}'.format(local_port=port, remote_port='29015'),change['new_val'][i]], _iter=True, _bg=True)
#            connections[name] = {'process':p,'port':port}
        except Exception as e:
            print(e)

async def watchFeed():
    print('monitoring for changes')
    while True:
        if q.empty():
            await asyncio.sleep(1)
        else:
            change = q.get(False)
            print('Restarting: '+change['new_val']['name'])
            print(change['new_val'])
            if not remoteMe['edgeNode']:
                sshTunnel(change)

async def log():
    while True:
        for key, value in connections.items():
            if not value['process'].empty():
                print("{}: {}".format(key, value['process'].read()))
        await asyncio.sleep(1)


def main():
    loop = asyncio.get_event_loop()
    asyncio.async(watchFeed())
    asyncio.async(log())
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()


#for change in feed:

