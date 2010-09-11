
import os
import time
from kokki import *

class EBSVolumeProvider(Provider):
    def action_create(self):
        if not self.resource.volume_id:
            raise Fail("Cannot create a volume with a speciic id (EC2 chooses volume ids)")

        nvid = self._volume_id_in_node_data()
        if nvid:
            # volume id is registered in the node data, so check that the volume in fact exists in EC2
            vol = self._volume_by_id(nvid)
            exists = vol and vol.status != "deleting"
            # TODO: determine whether this should be an error or just cause a new volume to be created. Currently erring on the side of failing loudly
            if not exists:
                raise Fail(
                    ("Volume with id %s is registered with the node but does not exist in EC2."
                     " To clear this error, remove the ['aws']['ebs_volume']['#{self.resource.name}']['volume_id'] entry from this node's data.") % (nvid,))
        else:
            # Determine if there is a volume that meets the resource's specifications and is attached to the current
            # instance in case a previous [:create, :attach] run created and attached a volume but for some reason was
            # not registered in the node data (e.g. an exception is thrown after the attach_volume request was accepted
            # by EC2, causing the node data to not be stored on the server)
            attached_volume = self.resource.device and self._currently_attached_volume(env.aws.instance_id, self.resource.device)
            if attached_volume:
                self.log.debug("There is already a volume attached at device %s" % self.resource.device)
                if not self._volume_compatible_with_resource_definition(attached_volume):
                    raise Fail("Volume %s attached at %s but does not conform to this resource's specifications" % (attached_volume['aws_id'], attached_volume['aws_device']))
                self.log.debug("The volume matches the resource's definition, so the volume is assumed to be already created")
                self.resource.env.aws.ebs_volume[self.resource.name]['volume_id'] = attached_volume['aws_id']
            else:
                # If not, create volume and register its id in the node data
                nvid = self._create_volume(self.resource.snapshot_id, self.resource.size, self.resource.availability_zone, self.resource.timeout)
                self.resource.env.aws.ebs_volume[self.resource.name]['volume_id'] = nvid
                self.resource.updated()

    def action_attach(self):
        vol = self._determine_volume()
 
        if vol.status == "in-use":
            if vol.attach_data.instance_id != env.aws.instance_id:
                raise Fail("Volume with id %s exists but is attached to instance %s" % (vol.id, vol.attach_data.instance_id))
            else:
                self.log.debug("Volume is already attached")
        else:
            # attach the volume and register its id in the node data
            self._attach_volume(vol.id, env.aws.instance_id, self.resource.device, self.resource.timeout)
            # self.resource.env.aws.ebs_volume[self.resource.name]['volume_id'] = vol.id
            self.resource.updated()

    def action_detach(self):
        vol = self._determine_volume()
        if not vol.attach_data or vol.attach_data.instance_id != env.aws.instance_id:
            return

        self._detach_volume(vol.id, self.resource.timeout)
        self.resource.updated()

    def action_snapshot(self):
        vol = self._determine_volume()
        snapshot = self.ec2.create_snapshot(vol.id)
        self.resource.updated()
        self.log.info("Created snapshot of %s as %s" % (vol.id, snapshot.id))

    def _volume_id_in_node_data(self):
        try:
            return self.resource.env.aws.ebs_volume[self.resource.name]['volume_id']
        except (KeyError, AttributeError):
            return None

    def _determine_volume(self):
        """Pulls the volume id from the volume_id attribute or the node data and verifies that the volume actually exists"""
        vol_id = self.resource.volume_id or self._volume_id_in_node_data() or (self.resource.device and self._currently_attached_volume(env.aws.instance_id, self.resource.device))
        if not vol_id:
            raise Fail("volume_id attribute not set and no volume id is set in the node data for this resource (which is populated by action create)")

        # check that volume exists
        vol = self._volume_by_id(vol_id)
        if not vol:
            raise Fail("No volume with id %s exists" % vol_id)

        return vol

    def _volume_by_id(self, volume_id):
        """Retrieves information for a volume"""
        volumes = self.ec2.get_all_volumes([volume_id])
        if volumes:
            return volumes[0]

    def _currently_attached_volume(self, instance_id, device):
        """Returns the volume that's attached to the instance at the given device or nil if none matches"""
        volumes = self.ec2.get_all_volumes()
        for v in volumes:
            if v.attach_data and v.attach_data.instance_id == instance_id and v.attach_data.device == device:
                return v

    # def volume_compatible_with_resource_definition?(volume)
    #     """Returns true if the given volume meets the resource's attributes"""
    #   (self.resource.size.nil? || self.resource.size == volume[:aws_size]) &&
    #   (self.resource.availability_zone.nil? || self.resource.availability_zone == volume[:zone]) &&
    #   (self.resource.snapshot_id == volume[:snapshot_id])
 
    # def create_volume(self, snapshot_id, size, availability_zone, timeout):
    #     """Creates a volume according to specifications and blocks until done (or times out)"""
    # 
    #     availability_zone = availability_zone or self.instance_availability_zone
    #     nv = ec2.create_volume(snapshot_id, size, availability_zone)
    #     Chef::Log.debug("Created new volume #{nv[:aws_id]}#{snapshot_id ? " based on #{snapshot_id}" : ""}")
    #  
    #   # block until created
    #   begin
    #     Timeout::timeout(timeout) do
    #       while true
    #         vol = volume_by_id(nv[:aws_id])
    #         if vol and vol[:aws_status] != "deleting"
    #           if ["in-use", "available"].include?(vol[:aws_status])
    #             Chef::Log.debug("Volume is available")
    #             break
    #           else
    #             Chef::Log.debug("Volume is #{vol[:aws_status]}")
    #           end
    #           sleep 3
    #         else
    #           raise "Volume #{nv[:aws_id]} no longer exists"
    #         end
    #       end
    #     end
    #   rescue Timeout::Error
    #     raise "Timed out waiting for volume creation after #{timeout} seconds"
    #   end
    #  
    #   nv[:aws_id]
 
    def _attach_volume(self, volume_id, instance_id, device, timeout):
        """Attaches the volume and blocks until done (or times out)"""
        self.log.info("Attaching %s as %s" % (volume_id, device))
        self.ec2.attach_volume(volume_id, instance_id, device)

        start_time = time.time()
        end_time = start_time + timeout if timeout else 0
        attached = False

        # block until attached
        while (not timeout) or (time.time() < end_time):
            vol = self._volume_by_id(volume_id)
            if vol and vol.status != "deleting":
                if vol.attachment_state() == "attached":
                    if vol.attach_data.instance_id == instance_id:
                        self.log.info("%s Volume is attached" % self)
                        attached = True
                        break
                    else:
                        raise Fail("Volume is attached to instance %s instead of %s" % (vol.attach_data.instance_id, instance_id))
                else:
                    self.log.debug("Volume is %s" % vol.status)
            else:
                raise Fail("%s Volume %s no longer exists" % (self, volume_id))
            time.sleep(3)

        # block until device is available
        if attached:
            while (not timeout) or (time.time() < end_time):
                if os.path.exists(self.resource.device):
                    return
                time.sleep(1)

        raise Fail("Timed out waiting for volume attachment after %s seconds" % (time.time() - start_time))

# # Detaches the volume and blocks until done (or times out)
# def detach_volume(volume_id, timeout)
#   Chef::Log.debug("Detaching #{volume_id}")
#   vol = volume_by_id(volume_id)
#   orig_instance_id = vol[:aws_instance_id]
#   ec2.detach_volume(volume_id)
#  
#   # block until detached
#   begin
#     Timeout::timeout(timeout) do
#       while true
#         vol = volume_by_id(volume_id)
#         if vol and vol[:aws_status] != "deleting"
#           if vol[:aws_instance_id] != orig_instance_id
#             Chef::Log.debug("Volume detached from #{orig_instance_id}")
#             break
#           else
#             Chef::Log.debug("Volume: #{vol.inspect}")
#           end
#         else
#           Chef::Log.debug("Volume #{volume_id} no longer exists")
#           break
#         end
#         sleep 3
#       end
#     end
#   rescue Timeout::Error
#     raise "Timed out waiting for volume detachment after #{timeout} seconds"

    @property
    def ec2(self):
        if hasattr(self, '_ec2'):
            return self._ec2

        from boto.ec2 import EC2Connection
        self._ec2 = EC2Connection(
            self.resource.aws_access_key or env.aws.access_key_id,
            self.resource.aws_secret_access_key or env.aws.secret_access_key)
        return self._ec2
