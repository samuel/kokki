
import os
from kokki import *

Package("debconf-utils")

Execute("apt-update-java",
    command = "apt-get update",
    action = "nothing")

if env.system.lsb['codename'] == 'karmic':
    def enter_the_multiverse():
        with open("/etc/apt/sources.list", "r") as fp:
            source = fp.read().split(' ')[1]
        return (
            "deb {source} karmic multiverse\n"
            "deb-src {source} karmic multiverse\n"
            "deb {source} karmic-updates multiverse\n"
            "deb-src {source} karmic-updates multiverse\n"
            "deb http://security.ubuntu.com/ubuntu karmic-security multiverse\n"
        ).format(source=source)
    File("/etc/apt/sources.list.d/multiverse",
        owner = "root",
        group = "root",
        mode = 0644,
        not_if = lambda:os.path.exists("/etc/apt/sources.list.d/multiverse"),
        content = enter_the_multiverse,
        notifies = [("run", env.resources["Execute"]["apt-update-java"], True)])

if env.system.lsb['codename'] == 'lucid':
    Execute('add-apt-repository "deb http://archive.canonical.com/ lucid partner" ; apt-get update',
        not_if = "grep 'lucid partner' /etc/apt/sources.list > /dev/null")

Script("accept-java-license",
    not_if = "debconf-show sun-java6-jre | grep accepted > /dev/null",
    cwd = "/usr/local/src",
    code = """#!/bin/sh
echo 'sun-java6-bin   shared/accepted-sun-dlj-v1-1    boolean true
sun-java6-jdk   shared/accepted-sun-dlj-v1-1    boolean true
sun-java6-jre   shared/accepted-sun-dlj-v1-1    boolean true
sun-java6-jre   sun-java6-jre/stopthread        boolean true
sun-java6-jre   sun-java6-jre/jcepolicy note
sun-java6-bin   shared/present-sun-dlj-v1-1     note
sun-java6-jdk   shared/present-sun-dlj-v1-1     note
sun-java6-jre   shared/present-sun-dlj-v1-1     note
'|debconf-set-selections""")
