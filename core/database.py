"""
Created on 2011-5-25

@author: archie
"""

#from pymongo import ReplicaSetConnection, ReadPreference, Connection

from pymongo import MongoClient, read_preferences
from config import config

def db_session():
    #return ReplicaSetConnection('%s:27017,%s:27017,%s:27017' % ('10.68.228.236', '10.68.228.232', '10.68.228.190'), replicaSet = 'bermuda_db', read_preference=ReadPreference.NEAREST)['bermuda']
    exec('connection = %s' % config.get('database', 'connection'))
    return connection['bermuda']

def query_db_session():
    #return ReplicaSetConnection('%s:27017,%s:27017,%s:27017' % ('10.68.228.190', '10.68.228.232', '10.68.228.236'), replicaSet = 'bermuda_db', read_preference=ReadPreference.SECONDARY_PREFERRED)['bermuda']
    exec('connection = %s' % config.get('database', 'query_connection'))
    return connection['bermuda']

def s1_db_session():
    '''
    shard1 DB
    '''
    exec('connection = %s' % config.get('database', 's1_connection'))
    return connection['bermuda_s1']


def multi_session():
    '''
    shard1 DB
    '''
    exec('connection = %s' % config.get('database', 'multi_connection'))
    return connection['bermuda_s1']
