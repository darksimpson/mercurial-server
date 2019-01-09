#!/bin/sh

set -e

BASEDIR=$(dirname "$0")

install -d /etc/mercurial-server/remote-hgrc.d
install -m 644 -t /etc/mercurial-server/remote-hgrc.d $BASEDIR/conf/remote-hgrc.d/access.rc $BASEDIR/conf/remote-hgrc.d/logging.rc

addgroup -S -g 150 hg
adduser -S -u 150 -D -s /bin/sh -G hg -h /var/lib/mercurial-server -g "Mercurial repositories" hg
usermod -p '*' hg

su -l -c "mkdir -p ~/.ssh && \
          cp $BASEDIR/conf/dot-mercurial-server ~/.mercurial-server" hg

cd $BASEDIR
python setup.py install --install-purelib=/usr/local/share/mercurial-server --install-platlib=/usr/local/share/mercurial-server --install-scripts=/usr/local/share/mercurial-server --install-data=/usr/local/share/mercurial-server
