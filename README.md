
Overview
========

Kokki is a system configuration management framework styled after Chef. It can
be used to build a full configuration system, but it also includes a basic
command line interface for simple uses.

As a Library
------------

    from kokki import *

    with Environment() as env:
        Package("vim", action="upgrade")
        File("/etc/hosts",
            owner = "root",
            group = "root",
            content =
                "127.0.0.1       localhost\n"
                "255.255.255.255 broadcasthost\n"
                "::1             localhost\n"
                "fe80::1%lo0     localhost\n")
        env.run()
