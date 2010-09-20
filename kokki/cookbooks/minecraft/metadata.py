
__description__ = "Minecraft game server"
__config__ = {
    "minecraft.path": dict(
        description = "Path where to install Minecraft server",
        default = "/var/lib/minecraft",
    ),
    "minecraft.user": dict(
        description = "User to run Minecraft server as",
        default = "nobody",
    ),
    "minecraft.package_url": dict(
        description = "URL of the server jar file",
        default = "http://www.minecraft.net/download/minecraft_server.jar", #"?v=445",
    ),
    "minecraft.xms": dict(
        description = "Initial Java heap size",
        default = "1024M",
    ),
    "minecraft.xmx": dict(
        description = "Maximum Java heap size",
        default = "1024M",
    ),
}
