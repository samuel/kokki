
from kokki import *

if env.system.platform in ("ubuntu", "debian"):
    Execute("wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -",
        not_if = "(apt-key list | grep 'Kohsuke Kawaguchi' > /dev/null)")
    

    apt = "deb http://pkg.jenkins-ci.org/debian binary/"
    apt_list_path = '/etc/apt/sources.list.d/jenkins.list'

    Execute("apt-update-jenkins",
        command = "apt-get update",
        action = "nothing")

    File(apt_list_path,
        owner = "root",
        group ="root",
        mode = 0644,
        content = apt+"\n",
        notifies = [("run", env.resources["Execute"]["apt-update-mongo"], True)])

Package("jenkins")
