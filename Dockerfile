FROM alpine:3.8

MAINTAINER darksimpson
LABEL version="1.0-ms1.3p1"
LABEL description="Dockerized minimal mercurial-server based on Alpine Linux"

RUN apk update && \
    apk --no-cache add shadow openssh-server mercurial

RUN deluser $(getent passwd 33 | cut -d: -f1) && \
    delgroup $(getent group 33 | cut -d: -f1) 2>/dev/null || true

RUN echo -e "AuthorizedKeysFile .ssh/authorized_keys\nPermitRootLogin no\nPasswordAuthentication no\nPort 8022\nPidFile none\n" > /etc/ssh/sshd_config

COPY ms /ms
RUN chown -R root:root /ms && \
    find /ms -type f -exec chmod 644 {} \; && \
    find /ms -type d -exec chmod 755 {} \; && \
    chmod 755 /ms/install.sh && \
    chmod 755 /ms/src/hg-ssh && \
    chmod 755 /ms/src/refresh-auth

RUN /ms/install.sh

RUN rm -rf /ms

COPY start.sh /start.sh
RUN chown root:root /start.sh && \
    chmod 755 /start.sh

VOLUME /etc/mercurial-server/keys
VOLUME /var/lib/mercurial-server/repos

EXPOSE 8022

CMD ["/start.sh"]
