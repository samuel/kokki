
__description__ = "Installs and configures Nginx"
__config__ = {
    "nginx.dir": dict(
        display_name = "Nginx Directory",
        description = "Location of nginx configuration files",
        default = "/etc/nginx",
    ),
    "nginx.log_dir": dict(
        display_name = "Nginx Log Directory",
        description = "Location for nginx logs",
        default = "/var/log/nginx",
    ),
    "nginx.log_format": dict(
        display_name = "Nginx Access Log Format",
        description = "Format string for the access log. If not set them the default for nginx is used.",
        default = None,
    ),
    "nginx.user": dict(
        display_name = "Nginx User",
        description = "User nginx will run as",
        default = "www-data",
    ),
    "nginx.binary": dict(
        display_name = "Nginx Binary",
        description = "Location of the nginx server binary",
        default = "/usr/sbin/nginx",
    ),
    "nginx.event_model": dict(
        display_name = "Nginx event model",
        description = "Which event model nginx should use (e.g. epoll)",
        default = None,
    ),
    "nginx.sendfile": dict(
        display_name = "Nginx Sendfile",
        description = "Wether sendfile should be used to serve files",
        default = True,
    ),
    "nginx.tcp_nopush": dict(
        display_name = "Nginx tcp_nopush",
        description = "Wether to enable/disable tcp_nopush",
        default = True,
    ),
    "nginx.tcp_nodelay": dict(
        display_name = "Nginx tcp_nodelay",
        description = "Wether to enable/disable tcp_nodelay",
        default = False,
    ),
    "nginx.gzip": dict(
        display_name = "Nginx Gzip",
        description = "Whether gzip is enabled",
        default = True,
    ),
    "nginx.gzip_http_version": dict(
        display_name = "Nginx Gzip HTTP Version",
        description = "Version of HTTP Gzip",
        default = 1.0,
    ),
    "nginx.gzip_comp_level": dict(
        display_name = "Nginx Gzip Compression Level",
        description = "Amount of compression to use",
        default = 2,
    ),
    "nginx.gzip_proxied": dict(
        display_name = "Nginx Gzip Proxied",
        description = "Whether gzip is proxied",
        default = "any",
    ),
    "nginx.gzip_types": dict(
        display_name = "Nginx Gzip Types",
        description = "Supported MIME-types for gzip",
        default = [
            "text/plain",
            "text/css",
            "application/x-javascript",
            "text/xml",
            "application/xml",
            "application/xml+rss",
            "text/javascript",
        ],
    ),
    "nginx.keepalive": dict(
        display_name = "Nginx Keepalive",
        description = "Whether to enable keepalive",
        default = True,
    ),
    "nginx.keepalive_timeout": dict(
        display_name = "Nginx Keepalive Timeout",
        default = 65,
    ),
    "nginx.worker_processes": dict(
        display_name = "Nginx Worker Processes",
        description = "Number of worker processes",
        default = 1,
    ),
    "nginx.worker_connections": dict(
        display_name = "Nginx Worker Connections",
        description = "Number of connections per worker",
        default = 1024,
    ),
    "nginx.server_names_hash_max_size": dict(
        display_name = "Nginx Maximum Server Names Hash Size",
        description = "The maximum size of the server name hash tables. (default 512)",
        default = None,
    ),
    "nginx.server_names_hash_bucket_size": dict(
        display_name = "Nginx Server Names Hash Bucket Size",
        description = "Directive assigns the size of basket in the hash-tables of the names of servers. (default 32/64/128 depending on architecture)",
        default = None,
    ),
}
