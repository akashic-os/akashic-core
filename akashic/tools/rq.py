"""
rq (rethinkdb-query) is a tool for querying rethinkdb, filtering rethinkdb, and finally saving your changes.
"""

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

