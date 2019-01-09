"""Mercurial access control hook"""

from mercurial.i18n import _
import mercurial.util
import mercurial.node

import os
from mercurialserver import ruleset
from mercurialserver import changes

def allow(ctx):
    branch = ctx.branch()
    if not ruleset.rules.allow("write", branch=branch, file=None):
        return False
    for f in ctx.files():
        if not ruleset.rules.allow("write", branch=branch, file=f):
            return False
    return True

def hook(ui, repo, hooktype, node=None, source=None, **kwargs):
    if hooktype != 'pretxnchangegroup':
        raise mercurial.util.Abort(_('config error - hook type "%s" cannot stop '
                           'incoming changesets') % hooktype)
    for ctx in changes.changes(repo, node):
        if not allow(ctx):
            raise mercurial.util.Abort(_('%s: access denied for changeset %s') %
                (__name__, mercurial.node.short(ctx.node())))

def phasehook(ui, repo, hooktype, **kwargs):
    if hooktype != 'prepushkey':
        raise mercurial.util.Abort(_('config error - hook type "%s" cannot stop '
                                     'incoming phase changes') % hooktype)
    if kwargs.get('namespace') == 'phases':
        if not ruleset.rules.allow("publish"):
            raise mercurial.util.Abort(_('%s: access denied for making %s public') %
                                       (__name__, kwargs['key'][:12]))
