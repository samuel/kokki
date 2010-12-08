
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

def lazyproperty(method):
    name = "_"+method.__name__
    @property
    def _lazyproperty(self):
        try:
            return getattr(self, name)
        except AttributeError:
            value = method(self)
            setattr(self, name, value)
            return value
    return _lazyproperty

class LazyAWS(object):
    def __init__(self, access_key_id, secret_access_key):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
    
    @lazyproperty
    def ec2(self):
        from boto.ec2 import EC2Connection
        self._ec2 = EC2Connection(
            self.access_key_id,
            self.secret_access_key)
        return self._ec2
    
    @lazyproperty
    def volumes(self):
        ec2 = self.ec2
        
        all_volumes = ec2.get_all_volumes()
        volumes = []
        for v in all_volumes:
            if v.attach_data and v.attach_data.instance_id == self.instance_id:
                volumes.append(v)
        return volumes
    
    def get_ec2_metadata(self, key):
        import urllib2
        res = urllib2.urlopen("http://169.254.169.254/2009-04-04/meta-data/" + key)
        return res.read().strip()
    
    @lazyproperty
    def instance_id(self):
        return self.get_ec2_metadata('instance-id')
    
    @lazyproperty
    def instance_type(self):
        return self.get_ec2_metadata('instance-type')
    
    @lazyproperty
    def availability_zone(self):
        return self.get_ec2_metadata('placement/availability-zone')

    @lazyproperty
    def tags(self):
        res = self.ec2.get_all_instances([self.instance_id])
        if not res:
            return {}
        return res.instances[0].tags

def __loader__(kit):
    aws = LazyAWS(
        kit.config.aws.access_key_id,
        kit.config.aws.secret_access_key
    )

    kit.update_config({
        "aws.resources": aws, 
        "aws.instance_id": aws.instance_id,
        "aws.instance_type": aws.instance_type,
        "aws.availability_zone": aws.availability_zone,
    })
