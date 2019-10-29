"""
Rewrite ~/.ssh/authorized_keys by recursing through key directories
"""

import re
import base64
import os, stat
import os.path
import subprocess
from mercurialserver import config

goodkey = re.compile("[/A-Za-z0-9._-]+$")

def refreshAuth():
    akeyfile = config.getAuthorizedKeysPath()
    wrappercommand = "/usr/bin/hg-ssh"
    prefix='no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command='

    if os.path.exists(akeyfile):
        f = open(akeyfile)
        try:
            for l in f:
                if not l.startswith(prefix):
                    raise Exception("Safety check failed, delete %s to continue" % akeyfile)
        finally:
            f.close()

    akeys = open(akeyfile + "_new", "w")
    for keyroot in config.getKeysPaths():
        kr = keyroot + "/"
        #print "Processing keyroot", keyroot
        for root, dirs, files in os.walk(keyroot):
            for fn in files:
                ffn = os.path.join(root, fn)
                if not ffn.startswith(kr):
                    raise Exception("Inconsistent behaviour in os.walk, bailing")
                #print "Processing file", ffn
                keyname = ffn[len(kr):]
                if not goodkey.match(keyname):
                    # Encode it for safe quoting
                    keyname = "--base64 " + base64.b64encode(keyname)
                p = subprocess.Popen(("ssh-keygen", "-i", "-f", ffn),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                newkey = p.communicate()[0]
                if p.wait() == 0:
                    klines = [l.strip() for l in newkey.split("\n")]
                else:
                    # Conversion failed, read it directly.
                    kf = open(ffn)
                    try:
                        klines = [l.strip() for l in kf]
                    finally:
                        kf.close()
                for l in klines:
                    if len(l):
                        akeys.write('%s"%s ~/repos/*" %s\n' % (prefix, wrappercommand, l))
    akeys.close()
    os.chmod(akeyfile + "_new", stat.S_IRUSR)
    os.rename(akeyfile + "_new", akeyfile)

def hook(ui, repo, hooktype, node=None, source=None, **kwargs):
    refreshAuth()
