#!/usr/bin/env python3
'''
Util script to copy the public key given in a yaml ConfigMap into the
authorized_hosts file for the sshd daemon user. Assumes config in the
form of


instances:
  key_name_1: instance_1
  key_name_2: instance_2
publick_keys:
  key_name_1: pubkey_1
  key_name_1: pubkey_2
'''
import yaml
from pathlib import Path
from os import environ
from sys import exit, argv

CONFIG_PATH = argv[1] # /etc/ssh.orig/key-mappings.yaml
AUTHORIZED_KEYS_PATH = argv[2] # /home/sshd-user/.ssh/authorized_keys
INSTANCE = environ['CE_INSTANCE']

with open(CONFIG_PATH) as f:
    config = yaml.load(f.read())

# Figure out to which instance our key belongs
# Instance dict is in the format key_name : instance
instances: dict[str, str] = config['instances']
for key_name, instance in instances.items():
    if instance == INSTANCE:
        break
else:
    print(f"Fatal: No key name found for instance {INSTANCE}.")
    exit(1)

AUTHORIZED_KEYS_PATH.parent.mkdir(parents=True, exist_ok=True)
pubkeys: dict[str, str] = config['public_keys']
pubkey = pubkeys.get(key_name)

if not pubkey:
    print(f"Fatal: No public key found for key {key_name}")
    exit(1)

with open(AUTHORIZED_KEYS_PATH, 'w') as keyf:
    keyf.write(pubkey)
