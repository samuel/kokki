
import os.path
from kokki import env, Group, User, Directory, File

env.include_recipe("ssh")

Group("sysadmin",
    gid = 2300)

for username, user in env.config.users.items():
    home = "/home/%s" % username

    User(username,
        uid = user['id'],
        home = home,
        groups = user.get('groups', []),
        password = user.get('password'))

    Directory(env.cookbooks.ssh.ssh_path_for_user(username),
        owner = username,
        group = username,
        mode = 0700)

    if user.get('sshkey'):
        env.cookbooks.ssh.SSHAuthorizedKey("%s-%s" % (username, user['sshkey_id']),
            user = username,
            keytype = user['sshkey_type'],
            key = user['sshkey'])
        File(os.path.join(env.cookbooks.ssh.ssh_path_for_user(username), "authorized_keys"),
            owner = username,
            group = username,
            mode = 0600)
