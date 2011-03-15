
__description__ = "Installs and configures Nginx"
__config__ = {
    "nginx.dir": dict(
        description = "Location of nginx configuration files",
        default = "/etc/nginx",
    ),
    "nginx.log_dir": dict(
        description = "Location for nginx logs",
        default = "/var/log/nginx",
    ),
    "nginx.log_format": dict(
        description = "Format string for the access log. If not set them the default for nginx is used.",
        default = None,
    ),
    "nginx.user": dict(
        description = "User nginx will run as",
        default = "www-data",
    ),
    "nginx.binary": dict(
        description = "Location of the nginx server binary",
        default = "/usr/sbin/nginx",
    ),
    "nginx.event_model": dict(
        description = "Which event model nginx should use (e.g. epoll)",
        default = None,
    ),
    "nginx.sendfile": dict(
        description = "Whether sendfile should be used to serve files",
        default = True,
    ),
    "nginx.tcp_nopush": dict(
        description = "Whether to enable/disable tcp_nopush",
        default = True,
    ),
    "nginx.tcp_nodelay": dict(
        description = "Whether to enable/disable tcp_nodelay",
        default = False,
    ),
    "nginx.gzip": dict(
        description = "Whether gzip is enabled",
        default = True,
    ),
    "nginx.gzip_http_version": dict(
        description = "Version of HTTP Gzip",
        default = 1.0,
    ),
    "nginx.gzip_comp_level": dict(
        description = "Amount of compression to use",
        default = 2,
    ),
    "nginx.gzip_proxied": dict(
        description = "Whether gzip is proxied",
        default = "any",
    ),
    "nginx.gzip_types": dict(
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
        description = "Whether to enable keepalive",
        default = True,
    ),
    "nginx.keepalive_timeout": dict(
        default = 65,
    ),
    "nginx.worker_processes": dict(
        description = "Number of worker processes",
        default = 1,
    ),
    "nginx.worker_connections": dict(
        description = "Number of connections per worker",
        default = 1024,
    ),
    "nginx.server_names_hash_max_size": dict(
        description = "The maximum size of the server name hash tables. (default 512)",
        default = None,
    ),
    "nginx.server_names_hash_bucket_size": dict(
        description = "Directive assigns the size of basket in the hash-tables of the names of servers. (default 32/64/128 depending on architecture)",
        default = None,
    ),
}
