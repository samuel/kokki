
from kokki import *

Package("debconf-utils")

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
