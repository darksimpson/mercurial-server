#!/bin/sh

set -e

if [ /etc/ssh/ssh_host_* 1> /dev/null 2>&1 ]; then
    echo "Generating host sshd keys"
    ssh-keygen -A
fi

if [ ! "$(stat -c %a /etc/mercurial-server/keys)" == "755" ]; then
    echo "Fixing permissions for keys volume"
    chmod 755 /etc/mercurial-server/keys
fi

if [ ! "$(stat -c %U /var/lib/mercurial-server/repos)" == "hg" ]; then
    echo "Fixing owner for repos volume"
    chown hg:hg /var/lib/mercurial-server/repos
fi

if [ ! "$(stat -c %a /var/lib/mercurial-server/repos)" == "755" ]; then
    echo "Fixing permissions for repos volume"
    chmod 755 /var/lib/mercurial-server/repos
fi

if [ ! -f /etc/mercurial-server/access.conf ]; then
    echo "Creating mercurial-server default access.conf"
    install -m 644 -t /etc/mercurial-server /usr/local/share/mercurial-server/conf/access.conf
fi

if [ ! -d /etc/mercurial-server/keys/root ]; then
    echo "Creating mercurial-server default keys/root directory"
    install -d /etc/mercurial-server/keys/root
fi

if [ ! -d /etc/mercurial-server/keys/users ]; then
    echo "Creating mercurial-server default keys/users directory"
    install -d /etc/mercurial-server/keys/users
fi

if [ ! -d /var/lib/mercurial-server/repos/hgadmin ]; then
    echo "Initializing mercurial-server hgadmin repo"
    su -l -c "mkdir -p /var/lib/mercurial-server/repos/hgadmin && \
              hg init /var/lib/mercurial-server/repos/hgadmin && \
              cp /usr/local/share/mercurial-server/conf/hgadmin-hgrc /var/lib/mercurial-server/repos/hgadmin/.hg/hgrc" hg
fi

echo "Refreshing mercurial-server auth keys"
su -l -c "/usr/local/share/mercurial-server/refresh-auth" hg

echo "Running mercurial-server sshd"
exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config
