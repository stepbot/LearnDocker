#!/bin/bash
# start.sh

# Start SSH daemon in the foreground
exec /usr/sbin/sshd -D
