"""
Find all the changes in a node in a way portable across Mercurial versions
"""

def changes(repo, node):
    start = repo[node].rev()
    try:
        end = len(repo.changelog)
    except:
        end = repo.changelog.count()
    for rev in xrange(start, end):
        yield repo[rev]
