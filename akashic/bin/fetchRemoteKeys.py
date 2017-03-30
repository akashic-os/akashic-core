#!/usr/bin/env python

'''
Use github to manage your ssh logins, since you probably already manage your keys with it.
Centralizing your key management should actually make you more secure,
presuming that you trust github and the infrastructure between you and them.
Including this script...
Run it without any args to see what users are allowed, which should help
you keep things secure.

It's *very* important that all allowed users actually own the github account with the same
username.

This aims to be a bit more secure then just using a shell script with

    curl -sf https://github.com/$1.keys

in it. All the permision code is in the `checkUser` function.

Always check what users are allowed by running `/opt/fetchRemoteKeys.py`

Configure as follows.
```
sudo groupadd gitusers
sudo usermode -a -G gitusers $SomeUserName

/opt/fetchRemoteKeys.py #Presuming you wgeted this script...

#/etc/sshd/sshd_config
AuthorizedKeysCommand      /opt/fetchRemoteKeys.py
AuthorizedKeysCommandUser  nobody

chmod 555 /opt/fetchRemoteKeys.py
chmod +x /opt/fetchRemoteKeys.py
chown root:root /opt/fetchRemoteKeys.py
```
'''

import grp, pwd, sys, requests

#Settings
allowedGroups= ['gitusers',]
disallowedGroups= []
keyString="https://github.com/{}.keys"#Keystring for github. There are probably other services that follow this methodology.


#Not-Settings
allowedGroupIDs = [obj.gr_gid for obj in grp.getgrall() if obj.gr_name in allowedGroups]
disallowedGroupIDs = [obj.gr_gid for obj in grp.getgrall() if obj.gr_name in disallowedGroups]

def get_additional_group_ids(username):
    return [g.gr_gid for g in grp.getgrall() if username in g.gr_mem]

def checkUser(username):
    userIsAllowed=False
    userGroups = get_additional_group_ids(username)
    for gid in userGroups:
        if gid in disallowedGroupIDs:
            userIsAllowed=False
            break
        if gid in allowedGroupIDs:
            userIsAllowed=True
    return userIsAllowed

if len(sys.argv)==2:
    if checkUser(sys.argv[1]):
        response = requests.get(keyString.format(sys.argv[1]), verify=True)
        if response.status_code == 200:
            print(response.text)

if len(sys.argv)==1:
    for user in pwd.getpwall():
        isallowed = checkUser(user.pw_name)
        if isallowed:
            sys.stdout.write('\u001b[32m')
        else:
            sys.stdout.write('\u001b[31m')
        print("{}, {}".format(user.pw_name, isallowed))
        sys.stdout.write('\u001b[39m')
