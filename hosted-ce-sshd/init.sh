#!/bin/bash

# Create a new directory to hold original SSH keys (if it doesn't yet exist)
mkdir -p /etc/ssh.orig/etc/ssh

# Generate a new set of SSH host keys for the container and copy them to the original location
ssh-keygen -A -f /etc/ssh.orig
/bin/cp -p /etc/ssh.orig/etc/ssh/* /etc/ssh/
chmod 400 /etc/ssh/*key

#Assume an authorized_keys file has been configured in /etc/ssh.orig/authorized_keys
mkdir -p /home/sshd-user/.ssh/
cp /etc/ssh.orig/authorized_keys /home/sshd-user/.ssh/authorized_keys
chown -R sshd-user /home/sshd-user/.ssh
chmod 600 /home/sshd-user/.ssh/authorized_keys

# Start sshd
/usr/sbin/sshd -e -D
