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
import socket, requests, time, asyncio, subprocess, tempfile, atexit, shutil
from marshmallow import Schema, fields, pprint
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
    remoteMe = [i for i in remoteMe][0]
    newMe = ChainMap(me, remoteMe, default)
elif remoteMe:
    remoteMe = remoteMe[0]
    newMe = ChainMap(me, remoteMe, default)
    r.table('dns').replace(newMe).run()

from multiprocessing import Process, Queue
def dnsFeed(q):
    #feed = r.table('dns').changes(include_initial=True).filter(lambda record:
    #    record["name"] == newMe['name']).run()
    feed = r.table('dns').changes(include_initial=True).run()
    for change in feed:
        q.put(change)

connections = {}

q = Queue()
p = Process(target=dnsFeed, args=(q,))
p.start()

tunnelPort = 23300 #Seems like an alright block.

socketFolder = tempfile.mkdtemp()
print(socketFolder)

class TunnelManager():
    def __init__(self, socketFolder, tunnelPort):
        self.connections = {}
        self.tunnelPort = tunnelPort
        self.socketFolder = socketFolder
    def __del__(self):
        for key in self.connections:
            self.deleteConnection(key)
        shutil.rmtree(self.socketFolder)

    def createConnection(self, name, localPort, remotePort, remoteIp):
        socketPath = "{}/akashic-ssh-Socket-{}".format(self.socketFolder,localPort)
#        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#        sock.bind(socketPath)
        forwardString = '{local_port}:localhost:{remote_port}'.format(local_port=localPort, remote_port=remotePort)
        p = subprocess.call(['ssh','-nNfS',socketPath,'-L',forwardString,remoteIp])
        if not p:
            self.connections[name]={'socketPath':socketPath,'localPort':localPort,'remotePort':remotePort,'remoteIp':remoteIp}
        else:
            raise Exception('failed to create ssh connection')
        return self

    def getPid(self, name):
        return subprocess.call(['ssh','-S',self.connections[name]['socketPath'],'-O','check','localhost'])

    def deleteConnection(self, name):
        subprocess.call(['ssh','-S',self.connections[name],'-O','exit','localhost'])
        del self.connections[name]
        return self

    def makeFromChangeSet(self, changeSet, remotePort):
        name = changeSet['new_val']['name']
        tryOrder = ['cjdns','lan','internet']
        if name in connections:
            localPort = connections[name]['port']
            socketPath = connections[name]['socketPath']
            subprocess.call(['ssh','-S',socketPath,'-O','exit','localhost'])
            del connections[name]
        else:
            localPort = self.tunnelPort
            self.tunnelPort = localPort+1

        for ipKey in tryOrder:
            try:
                self.createConnection(name, localPort, remotePort, changeSet['new_val'][ipKey])
                break
            except Exception as e:
                print(e)
        print(self.connections)
        print(self.getPid(name))

def sshTunnel(change):
    global tunnelPort
    name = change['new_val']['name']
    tryOrder = ['cjdns','lan','internet']
    if name in connections:
        port = connections[name]['port']
        socketPath = "{}/akashic-ssh-Socket-{}".format(socketFolder,port)
        subprocess.call(['ssh','-S','socketPath','-O','exit','localhost'])
        del connections[name]
    else:
        port = tunnelPort
        tunnelPort = tunnelPort+1
    for ipKey in tryOrder:
        remote_port="29015"
        remote_port="8080"
        socketPath = "{}/akashic-ssh-Socket-{}".format(socketFolder,port)
        forwardString = '{local_port}:localhost:{remote_port}'.format(local_port=port, remote_port=remote_port)
        ipToTry = str(change['new_val'][ipKey])
        p = subprocess.call(['ssh','-nNfS',socketPath,'-L',forwardString,ipToTry])
        if not p:
            print(subprocess.call(['ssh','-S',socketPath,'-O','check','localhost']))
            connections[name] = {'socket':socketPath,'port':port}
            break

tunnelManager = TunnelManager(tempfile.mkdtemp(),23300)

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
                tunnelManager.makeFromChangeSet(change, 8080)

#Clean everything up.
def exit():
    shutil.rmtree(socketFolder)

atexit.register(exit)

def main():
    loop = asyncio.get_event_loop()
    asyncio.async(watchFeed())
#    asyncio.async(log())
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()


#for change in feed:

