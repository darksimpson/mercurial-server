"""
Hook to log changesets pushed and pulled
"""

from mercurial.i18n import _
import mercurial.util
import mercurial.node

import os
import time
import fcntl

try:
    import json
    json.dumps
except ImportError:
    import simplejson as json

from mercurialserver import ruleset, changes

def writelog(repo, op, **kw):
    """Write a log entry in the mercurial-server log file as a JSON
    formatted dict.

    op is the operation (typically 'push', 'pull' or 'publish') 

    any element in the kw argument is also added in the log entry
    dictionnary.
    """
    logentry = kw.copy()
    logentry.update(dict(
        timestamp=time.strftime("%Y-%m-%d_%H:%M:%S Z", time.gmtime()),
        op=op,
        key=ruleset.rules.get('user'),
        ssh_connection=os.environ['SSH_CONNECTION'],))
    with open(repo.vfs.join("mercurial-server.log"), "a+") as log:
        fcntl.flock(log.fileno(), fcntl.LOCK_EX)
        log.seek(0, os.SEEK_END)
        # YAML log file format
        log.write("- %s\n" % json.dumps(logentry))
    
def hook(ui, repo, hooktype, node=None, source=None, **kwargs):
    if hooktype == 'changegroup':
        op = "push"
    elif hooktype == 'outgoing':
        op = "pull"
    else:
        raise mercurial.util.Abort(_('servelog.hook installed as wrong hook type,'
                                     ' must be changegroup or outgoing but is %s') % hooktype)
    writelog(repo, op, 
             nodes=[mercurial.node.hex(ctx.node())
                    for ctx in changes.changes(repo, node)])

def phaseshook(ui, repo, hooktype, node=None, source=None, **kwargs):
    if hooktype == 'pushkey':
        if kwargs.get('namespace') == 'phases':
            writelog(repo, 'publish', nodes=[kwargs['key']])
    else:
        raise mercurial.util.Abort(_('servelog.phaseshook installed as wrong hook type,'
                                     ' must be pushkey but is %s') % hooktype)
        
