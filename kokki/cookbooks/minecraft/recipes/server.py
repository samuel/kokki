
import os
from kokki import *

env.include_recipe("java.jre")

Package("screen")

Directory(env.config.minecraft.path,
    owner = env.config.minecraft.user)

Script("install-minecraft-server",
    not_if = lambda:os.path.exists(os.path.join(env.config.minecraft.path, "minecraft_server.jar")),
    code = (
        "cd {config.minecraft.path}\n"
        "wget {config.minecraft.package_url}\n"
    ).format(config=env.config)
)

File("%s/server.sh",
    mode = 0755,
    content = (
        "#!/bin/sh\n"
        "cd {0}\n"
        "java -Xmx1024M -Xms1024M -jar {0}/minecraft_server.jar nogui\n"
    ).format(env.config.minecraft.path),
)

Service("minecraft-server",
    start_command = "screen -dmS minecraft -- %s/server.sh" % env.config.minecraft.path,
    stop_command = 'screen -S minecraft -X stuff "stop\n"',
    status_command = "nc -z localhost 25565",
    action = "start",
)
