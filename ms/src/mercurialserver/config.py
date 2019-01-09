"""
Fix $HOME and read ~/.mercurial-server
"""

import sys
import os
import os.path
import pwd
import ConfigParser

globalconfig = None

def _getConf():
    global globalconfig
    if globalconfig is None:
        globalconfig = ConfigParser.RawConfigParser()
        globalconfig.read(os.path.expanduser("~/.mercurial-server"))
    return globalconfig

def _getPath(name):
    return os.path.expanduser(_getConf().get("paths", name))

def _getPaths(name):
    return [os.path.expanduser(p)
        for p in _getConf().get("paths", name).split(":")]

def getReposPath(): return _getPath("repos")
def getAuthorizedKeysPath(): return _getPath("authorized_keys")

def configExists():
    try:
        getAuthorizedKeysPath()
        return True
    except Exception, e:
        print e
        return False

def getKeysPaths(): return _getPaths("keys")
def getAccessPaths(): return _getPaths("access")

def getEnv(): return _getConf().items("env")

def _getdefault(section, option, default, f = lambda x: x):
    conf = _getConf()
    if conf.has_option(section, option):
        return f(conf.get(section, option))
    else:
        return default

def getAllowedDots():
    return _getdefault("exceptions", "allowdots", [],
        lambda s: s.split(":"))

# Work out where we are, don't use config.
def initExe():
    global _exePath
    _exePath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # Fix $HOME in case of "sudo -u hg refresh-auth"
    os.environ['HOME'] = pwd.getpwuid(os.geteuid()).pw_dir

def getExePath():
    return _exePath
