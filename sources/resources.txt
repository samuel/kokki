==============
Resource Types
==============

File
====

action
    create(default), delete, touch
path
    String: Path to the file (defaults to 'name')
backup
    Boolean: Create a backup of any replaced files (unimplemented)
mode
    Integer: Numerical mode for the file
owner
    String/Integer: UID or username
group
    String/Integer: GID or groupname
content
    Source: Template or string

Directory
=========

action
    create(default), delete
path
    String: Path to the directory (defaults to 'name')
mode
    Integer: Numerical mode for the file
owner
    String/Integer: UID or username
group
    String/Integer: GID or groupname
recursive
    Boolean: Recursively create or delete the folder and it's parents (default False)

Link
====

action
    create(default), delete
path
    String: Path to the link (defaults to 'name')
to
    String: Path to the file or directory to link to
hard
    Boolean: Create a hard link (default False)

Execute
=======

action
    run(default)
command
    String: Command to execute (defaults to 'name')
creates
    String: Path to a file or directory that is created by the command. If the path exists then don't execute the command.
cwd
    String: Working directory when executing the command
environment:
    Dict: Extra environment variables
user:
    String/Integer: UID or username to run the command as (unimplemented)
group:
    String/Integer: GID or groupname to run the command as (unimplemented)
returns:
    Integer: Expected return value for success (default 0)
timeout:
    Integer: Max number of seconds the command is allowed to execute for (unimplemented)

Script
======

action
    run(default)
code
    String: Shell script
cwd
    String: Working directory when executing the script
interpreter
    String: Interpreter to run the script with (default /bin/bash)

Mount
=====

action
    mount(default), umount, remount, enable, disable
mount_point
    String: Path to the mount point (defaults to 'name')
device
    String: Device to mount
fstype
    String: Filesystem type
options
    List: List of options given to mount (default ["defaults"])
dump
    Integer: dump value in fstab (default 0)
passno
    Integer: passno value in fstab (default 2)

Package
=======

action
    install(default), upgrade, remove, purge
package_name
    String: Name of package (defaults to 'name')
version
    String: Version of package to install
