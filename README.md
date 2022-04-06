# libvirt_cgroups

A simple python script to create symbolic links to the machine-qemu cgroup directories. 

As much as I've tried, I can not get the telegraf cgroup plugin to read the native cgroup
directories that are created by virt-manager/libvirt. My hypothesis is that it does not
handle the \xd2 escape sequence in the directory names (minus sign) which is used instead
of a normal ascii-dash for some reason.  This script creates (and updates) matching
symbolic links to the /libvirt_cgroups/ directory, so that the telegraf plugin can
be pointed to this directory instead of the normal /sys/fs/...  directory to obtain
libvirt vm statistics like cpu and memory usage.

## install
1) create the /libvirt_cgroups/ directory

2) schedule a cron job to execute this script
