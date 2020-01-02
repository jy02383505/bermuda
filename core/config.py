import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/Application/bermuda/conf/bermuda.conf')

def initConfig():
    config = ConfigParser.RawConfigParser()
    config.read('/Application/bermuda/conf/bermuda.conf')
    return config