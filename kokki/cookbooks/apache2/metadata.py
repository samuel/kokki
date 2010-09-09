
__description__ = "Apache2 web server"
__config__ = {
    "apache.dir": {
        "description": "Location for Apache configuration",
        "default": "/etc/apache2",
    },
    "apache.log_dir": {
        "description": "Location for Apache logs",
        "default": "/etc/apache2",
    },
    "apache.user": {
        "description": "User Apache runs as",
        "default": "www-data",
    },
    "apache.binary": {
        "description": "Apache server daemon program",
        "default": "/usr/sbin/apache2",
    },
    "apache.icondir": {
        "description": "Directory location for icons",
        "default": "/usr/share/apache2/icons",
    },
    "apache.listen_ports": {
        "description": "Ports that Apache should listen on",
        "default": [80, 443],
    },
    "apache.contact": {
        "description": "Email address of webmaster",
        "default": "ops@example.com",
    },
    "apache.timeout": {
        "description": "Connection timeout value",
        "default": 300,
    },
    "apache.keepalive": {
        "description": "HTTP persistent connections",
        "default": "On",
    },
    "apache.keepaliverequests": {
        "description": "Number of requests allowed on a persistent connection",
        "default": 100,
    },
    "apache.keepalivetimeout": {
        "description": "Time to wait for requests on persistent connection",
        "default": 5,
    },
    "apache.servertokens": {
        "display_name": "Apache Server Tokens",
        "description": "Server response header",
        "default": "Prod",
    },
    "apache.serversignature": {
        "display_name": "Apache Server Signature",
        "description": "Configure footer on server-generated documents",
        "default": "Off",
    },
    "apache.traceenable": {
        "display_name": "Apache Trace Enable",
        "description": "Determine behavior of TRACE requests",
        "default": "Off",
    },
    "apache.allowed_openids": {
        "display_name": "Apache Allowed OpenIDs",
        "description": "Array of OpenIDs allowed to authenticate",
        "default": None,
    },
    "apache.prefork.startservers": {
        "display_name": "Apache Prefork MPM StartServers",
        "description": "Number of MPM servers to start",
        "default": 16,
    },
    "apache.prefork.minspareservers": {
        "display_name": "Apache Prefork MPM MinSpareServers",
        "description": "Minimum number of spare server processes",
        "default": 16,
    },
    "apache.prefork.maxspareservers": {
        "display_name": "Apache Prefork MPM MaxSpareServers",
        "description": "Maximum number of spare server processes",
        "default": 32,
    },
    "apache.prefork.serverlimit": {
        "display_name": "Apache Prefork MPM ServerLimit",
        "description": "Upper limit on configurable server processes",
        "default": 400,
    },
    "apache.prefork.maxclients": {
        "display_name": "Apache Prefork MPM MaxClients",
        "description": "Maximum number of simultaneous connections",
        "default": 400,
    },
    "apache.prefork.maxrequestsperchild": {
        "display_name": "Apache Prefork MPM MaxRequestsPerChild",
        "description": "Maximum number of request a child process will handle",
        "default": 10000,
    },
    "apache.worker.startservers": {
        "display_name": "Apache Worker MPM StartServers",
        "description": "Initial number of server processes to start",
        "default": 4,
    },
    "apache.worker.maxclients": {
        "display_name": "Apache Worker MPM MaxClients",
        "description": "Maximum number of simultaneous connections",
        "default": 1024,
    },
    "apache.worker.minsparethreads": {
        "display_name": "Apache Worker MPM MinSpareThreads",
        "description": "Minimum number of spare worker threads",
        "default": 64,
    },
    "apache.worker.maxsparethreads": {
        "display_name": "Apache Worker MPM MaxSpareThreads",
        "description": "Maximum number of spare worker threads",
        "default": 192,
    },
    "apache.worker.threadsperchild": {
        "display_name": "Apache Worker MPM ThreadsPerChild",
        "description": "Constant number of worker threads in each server process",
        "default": 64,
    },
    "apache.worker.maxrequestsperchild": {
        "display_name": "Apache Worker MPM MaxRequestsPerChild",
        "description": "Maximum number of request a child process will handle",
        "default": 0,
    },
}

# Where the various parts of apache are
if system.platform in ('redhat', 'centos', 'fedora', 'suse'):
    updates = {
        "apache.dir":     "/etc/httpd",
        "apache.log_dir": "/var/log/httpd",
        "apache.user":    "apache",
        "apache.binary":  "/usr/sbin/httpd",
        "apache.icondir": "/var/www/icons/",
    }
else: # env.system.platform in ("debian", "ubuntu"):
    updates = {
        "apache.dir":     "/etc/apache2",
        "apache.log_dir": "/var/log/apache2",
        "apache.user":    "www-data",
        "apache.binary":  "/usr/sbin/apache2",
        "apache.icondir": "/usr/share/apache2/icons",
    }
for k, v in updates.items():
    __config__[k]['default'] = v
