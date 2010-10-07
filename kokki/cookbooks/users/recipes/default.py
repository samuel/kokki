
import os.path
from kokki import *

env.include_recipe("ssh")

Group("sysadmin",
    gid = 2300)

for user in env.config.users:
    home = "/home/%s" % user['username']

    User(user['username'],
        uid = user['id'],
        home = home,
        groups = user.get('groups', []),
        password = user.get('password'))

    Directory(env.cookbooks.ssh.ssh_path_for_user(user['username']),
        owner = user['username'],
        group = user['username'],
        mode = 0700)

    if user.get('sshkey'):
        env.cookbooks.ssh.SSHAuthorizedKey("%s-%s" % (user['username'], user['sshkey_id']),
            user = user['username'],
            keytype = user['sshkey_type'],
            key = user['sshkey'])
        File(os.path.join(env.cookbooks.ssh.ssh_path_for_user(user['username']), "authorized_keys"),
            owner = user['username'],
            group = user['username'],
            mode = 0600)
