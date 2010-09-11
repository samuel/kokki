
__description__ = "Resources and providers to support Amazon's Web Services (EC2, S3, etc..)"
__config__ = {
    "aws.access_key_id": dict(
        description = "API Key for AWS",
        default = None,
    ),
    "aws.secret_access_key": dict(
        description = "Secret key for AWS",
        default = None,
    ),
    "aws.volumes": dict(
        description = "Volumes to attach and mount to the current instance (volume_id, device, fstype, fsoptions, mount_point)",
        default = [],
    ),
}
