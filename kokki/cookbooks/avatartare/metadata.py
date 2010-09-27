
__description__ = "Avatar server"
__config__ = {
    "avatartare.path": dict(
        display_name = "Avatartare path",
        description = "Path to avatartare installation",
        default = "/var/www/avatartare",
    ),
    "avatartare.aws_access_key_id": dict(
        display_name = "AWS Access Key ID",
        description = "AWS key to use for S3",
        default = None,
    ),
    avatartare.aws_secret_access_key: dict(
        display_name = "AWS Secret Access Key",
        description = "AWS secret key to use for S3",
        default = None,
    ),
    avatartare.s3_bucket: dict(
        display_name = "S3 bucket",
        description = "S3 bucket where to store avatars",
        default = "avatartare",
    ),
    avatartare.memcached_servers: dict(
        display_name = "Memcached Servers",
        description = "List of memcached servers to use",
        default = ["localhost:11211"],
    ),
    avatartare.process_count: dict(
        display_name = "Process Count",
        description = "Number of processes to run",
        default = 6,
    ),
}
