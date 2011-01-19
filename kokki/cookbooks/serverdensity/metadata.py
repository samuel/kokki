
__description__ = "ServerDensity server monitoring"
__config__ = {
    "serverdensity.agent_key": dict(
        description = "Agent key",
        default = "key",
    ),
    "serverdensity.sd_url": dict(
        description = "Service url",
        default = "http://name.serverdensity.com",
    ),
    "serverdensity.configs": dict(
        description = "Dictionary of additional config variables for sd-agent",
        default = {},
    ),
}
