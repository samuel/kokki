
__description__ = "Avatar server"
__config__ = {
    "avatartare.path": dict(
        description = "Path to avatartare installation",
        default = "/var/www/avatartare",
    ),
    "avatartare.aws_access_key_id": dict(
        description = "AWS key to use for S3",
        default = None,
    ),
    "avatartare.aws_secret_access_key": dict(
        description = "AWS secret key to use for S3",
        default = None,
    ),
    "avatartare.s3_bucket": dict(
        description = "S3 bucket where to store avatars",
        default = "avatartare",
    ),
    "avatartare.memcached_servers": dict(
        description = "List of memcached servers to use",
        default = ["localhost:11211"],
    ),
    "avatartare.process_count": dict(
        description = "Number of processes to run",
        default = 6,
    ),
}
