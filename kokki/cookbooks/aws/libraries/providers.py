
import itertools
import os
import time
from kokki import Provider, Fail

class EBSVolumeProvider(Provider):
    def action_create(self):
        if self.resource.volume_id:
            raise Fail("Cannot create a volume with a specific id (EC2 chooses volume ids)")
        
        vol = self._find_volume(self.resource.volume_id, self.resource.name, self.resource.device)
        if vol:
            self.log.debug("Volume %s already exists", self.resource)
            # self.log.debug("There is already a volume attached at device %s" % self.resource.device)
            # # if not self._volume_compatible_with_resource_definition(attached_volume):
            # raise Fail("Volume %s attached at %s but does not conform to this resource's specifications" % (attached_volume['aws_id'], attached_volume['aws_device']))
            # # self.log.debug("The volume matches the resource's definition, so the volume is assumed to be already created")
        else:
            vol = self._create_volume(self.resource.snapshot_id, self.resource.size, self.resource.availability_zone, self.resource.name, self.resource.timeout)
            self.resource.updated()
    
    def action_attach(self):
        vol = self._determine_volume()
        
        if vol.status == "in-use":
            if vol.attach_data.instance_id != self.resource.env.config.aws.instance_id:
                raise Fail("Volume with id %s exists but is attached to instance %s" % (vol.id, vol.attach_data.instance_id))
            else:
                self.log.debug("Volume is already attached")
        else:
            self._attach_volume(vol, self.resource.env.config.aws.instance_id, self.resource.device, self.resource.timeout)
            self.resource.updated()
    
    def action_detach(self):
        vol = self._determine_volume()
        if not vol.attach_data or vol.attach_data.instance_id != self.resource.env.config.aws.instance_id:
            return
        
        self._detach_volume(vol, self.resource.timeout)
        self.resource.updated()
    
    def action_snapshot(self):
        vol = self._determine_volume()
        snapshot = self.ec2.create_snapshot(vol.id)
        self.resource.updated()
        self.log.info("Created snapshot of %s as %s" % (vol.id, snapshot.id))
    
    def _find_volume(self, volume_id=None, name=None, device=None):
        vol = None
        if volume_id:
            vol = self._volume_by_id(volume_id)
        else:
            all_volumes = [v for v in self.ec2.get_all_volumes() if v.status in ('in-use', 'available')]
            if device:
                for v in all_volumes:
                    if v.attach_data and v.attach_data.device == device and v.attach_data.instance_id == self.resource.env.config.aws.instance_id:
                        vol = v
                        break
            if not vol and name:
                if '{index}' in name:
                    allnames = dict((v.tags.get('Name'), v) for v in all_volumes)
                    for i in itertools.count(1):
                        vname = name.format(index=i)
                        try:
                            v = allnames[vname]
                            if v.status == "available":
                                vol = v
                                break
                        except KeyError:
                            self.resource.name = vname
                            break
                else:
                    for v in all_volumes:
                        if v.tags.get('Name') == name:
                            vol = v
                            break
        if vol and '{index}' in name:
            self.resource.name = vol.tags.get('Name')
        return vol

    def _determine_volume(self):
        """Pulls the volume id from the volume_id attribute or the node data and verifies that the volume actually exists"""
        vol = self._find_volume(self.resource.volume_id, self.resource.name, self.resource.device)

        if not vol:
            raise Fail("volume_id attribute not set or no volume with the given name or device found")

        return vol

    def _volume_by_id(self, volume_id):
        """Retrieves information for a volume"""
        volumes = self.ec2.get_all_volumes([volume_id])
        if volumes:
            return volumes[0]

    def _volume_compatible_with_resource_definition(self, volume):
        return (
            (not self.resource.size or self.resource.size == volume.size),
            (not self.resource.availability_zone or self.resource.availability_zone == volume.zone),
            (self.resource.snapshot_id == volume.snapshot_id)
        )
    
    def _find_snapshot(self, name):
        snapshots = self.ec2.get_all_snapshots(filters={"tag:Name": name})
        if snapshots:
            snapshots.sort(cmp=lambda x, y: cmp(y.start_time, x.start_time))
            return snapshots[0]
        return None
    
    def _create_volume(self, snapshot_id, size, availability_zone, name, timeout):
        """Creates a volume according to specifications and blocks until done (or times out)"""

        self.log.debug("Creating volume with attributes: snapshot_id=%s size=%s availability_zone=%s name=%s timeout=%s", snapshot_id, size, availability_zone, name, timeout)

        if snapshot_id and not snapshot_id.startswith('snap-'):
            sid = self._find_snapshot(snapshot_id)
            if not sid and self.resource.snapshot_required:
                raise Fail("Unable to find snapshot with name %s" % snapshot_id)
            snapshot_id = sid

        availability_zone = availability_zone or self.resource.env.config.aws.availability_zone
        vol = self.ec2.create_volume(size, availability_zone, snapshot_id)
        self.log.info("Created new volume %s %s%s", name, vol.id, " based on %s" % snapshot_id if snapshot_id else "")

        start_time = time.time()
        end_time = start_time + timeout if timeout else 0

        while (not timeout) or (time.time() < end_time):
            if vol.update() in ('in-use', 'available'):
                break
            time.sleep(1)

        if name:
            vol.add_tag('Name', name)

        try:
            del self.resource.env.config.aws.resources._volumes
        except AttributeError:
            pass

        return vol

    def _attach_volume(self, vol, instance_id, device, timeout):
        """Attaches the volume and blocks until done (or times out)"""
        self.log.info("Attaching %s as %s" % (vol.id, device))
        vol.attach(instance_id, device)

        start_time = time.time()
        end_time = start_time + timeout if timeout else 0
        attached = False

        # block until attached
        while (not timeout) or (time.time() < end_time):
            if vol.update() != "deleting":
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
                raise Fail("%s Volume %s no longer exists" % (self, vol.id))
            time.sleep(3)

        # block until device is available
        if attached:
            while (not timeout) or (time.time() < end_time):
                if os.path.exists(self.resource.device):
                    return
                time.sleep(1)

        raise Fail("Timed out waiting for volume attachment after %s seconds" % (time.time() - start_time))

    # def detach_volume(self, vol, timeout):
    #     Chef::Log.debug("Detaching #{volume_id}")
    #     vol = volume_by_id(volume_id)
    #     orig_instance_id = vol[:aws_instance_id]
    #     vol.detach()
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
        return self.resource.env.config.aws.resources.ec2
