
__description__ = "Software RAID for Linux"
__config__ = {
    "mdadm.arrays": dict(
        description = "List of dictionary with keys name, devices, level, chunksize, and metadata",
        default = [],
    ),
}
