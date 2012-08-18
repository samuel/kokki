import os
from kokki import Execute, Package

# if not (env.system.platform == "ubuntu" and env.system.lsb['release'] in ["11.10"]):
#     apt_list_path = '/etc/apt/sources.list.d/pitti-postgresql-lucid.list'

#     Execute("apt-update-postgresql9",
#         command = "apt-get update",
#         action = "nothing")

#     apt = None
#     if env.system.platform == "ubuntu":
#         Package("python-software-properties")
#         Execute("add-apt-repository ppa:pitti/postgresql -y",
#             not_if = lambda:os.path.exists(apt_list_path),
#             notifies = [("run", env.resources["Execute"]["apt-update-postgresql9"], True)])
