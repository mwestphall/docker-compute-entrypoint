FROM almalinux:9

RUN yum install -y openssh-server && \
    yum clean all && \
    rm -rf /var/cache/yum/ && \
    adduser sshd-user

COPY init.sh /usr/local/sbin

CMD [ "/usr/local/sbin/init.sh" ]
