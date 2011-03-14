
from kokki import Package, Execute

Package("erlang")

if env.system.platform in ("ubuntu", "debian"):
    pkg_url = "http://www.rabbitmq.com/releases/rabbitmq-server/v2.3.1/rabbitmq-server_2.3.1-1_all.deb"
    Execute("cd /tmp ; wget %s ; dpkg -i %s ; rm rabbitmq*deb" % (pkg_url, pkg_url.rsplit('/', 1)[-1]),
        not_if = "dpkg-query -c rabbitmq-server > /dev/null")

