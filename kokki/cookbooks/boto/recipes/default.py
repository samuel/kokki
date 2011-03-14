
from kokki import Package

# Package("python-boto")

# Package("pip",
#     provider = "kokki.providers.package.easy_install.EasyInstallProvider")
# Execute("mv /usr/lib/pymodules/python2.6/boto /tmp/boto.orig",
#     only_if = lambda:os.path.exists("/usr/lib/pymodules/python2.6/boto"))
# Execute("pip install git+http://github.com/boto/boto.git#egg=boto",
#     not_if = 'python -c "import boto"')

Package("boto",
    action = "upgrade",
    provider = "kokki.providers.package.easy_install.EasyInstallProvider")
