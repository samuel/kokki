
__description__ = "CloudKick server monitoring"
__config__ = {
    "cloudkick.oauth_key": dict(
        description = "OAuth Key",
        default = None,
    ),
    "cloudkick.oath_secret": dict(
        description = "OAuth Secret",
        default = None,
    ),
    "cloudkick.tags": dict(
        description = "Tags",
        default = [],
    ),
    "cloudkick.hostname": dict(
        description = "Hostname",
        default = None,
    ),
}
