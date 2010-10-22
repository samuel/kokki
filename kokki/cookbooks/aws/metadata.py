
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

# import urllib2
# def get_ec2_metadata(key):
#     res = urllib2.urlopen("http://169.254.169.254/2008-02-01/meta-data/" + key)
#     return res.read().strip()
# 
# __config__.update({
#     "aws.instance_id": dict(
#         default = get_ec2_metadata('instance-id'),
#     ),
#     "aws.instance_type": dict(
#         default = get_ec2_metadata('instance-type'),
#     ),
#     "aws.availability_zone": dict(
#         default = get_ec2_metadata('placement/availability-zone'),
#     ),
# })
