
import hashlib
import hmac
import os
from base64 import b64decode, b64encode
from kokki import Fail, Environment

class SSHKnownHostsFile(object):
    def __init__(self, path=None):
        self.hosts = []
        self.parse(path)

    def parse(self, path):
        self.hosts = []
        with open(path, "r") as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue

                addr, keytype, key = line.split(' ')
                if addr.startswith('|1|'):
                    # Hashed host entry
                    salt, hosthash = addr.split('|')[2:]
                    self.hosts.append((1, b64decode(salt), b64decode(hosthash), keytype, key))
                else:
                    # Unhashed
                    for a in addr.split(','):
                        self.hosts.append((0, a, keytype, key))

    def save(self, path):
        with open(path, "w") as fp:
            fp.write(str(self))

    def includes(self, host):
        host = host.lower()
        for h in self.hosts:
            if h[0] == 0:
                if h[1] == host:
                    return True
            elif h[0] == 1:
                hosthash = self.hash(host, h[1])[0]
                if hosthash == h[2]:
                    return  True
        return False

    def hash(self, host, salt=None):
        if not salt:
            salt = self.generate_salt()
        return hmac.new(salt, host, digestmod=hashlib.sha1).digest(), salt

    def generate_salt(self):
        return os.urandom(20)

    def add_host(self, host, keytype, key, hashed=True, verify=True):
        host = host.lower()
        if verify and self.includes(host):
            return False

        if hashed:
            hosthash, salt = self.hash(host)
            self.hosts.append((1, salt, hosthash, keytype, key))
        else:
            self.hosts.append((0, host, keytype, key))

        return True

    def remove_host(self, host):
        host = host.lower()
        new_hosts = []
        for h in self.hosts:
            if h[0] == 0:
                if h[1] == host:
                    continue
            elif h[0] == 1:
                hosthash = self.hash(host, h[1])[0]
                if hosthash == h[2]:
                    continue
            new_hosts.append(h)

        found = len(new_hosts) != len(self.hosts)
        self.hosts = new_hosts
        return found

    def __str__(self):
        out = []
        unhashed = {} # Group unhashed hosts by the key
        for h in self.hosts:
            if h[0] == 0:
                k = (h[2], h[3])
                if k not in unhashed:
                    unhashed[k] = [h[1]]
                else:
                    unhashed[k].append(h[1])
            elif h[0] == 1:
                out.append("|1|%s|%s %s %s" % (b64encode(h[1]), b64encode(h[2]), h[3], h[4]))
        for k, host in unhashed.items():
            out.append("%s %s %s" % (",".join(host), k[0], k[1]))
        out.append("")
        return "\n".join(out)

class SSHAuthorizedKeysFile(object):
    def __init__(self, path=None):
        self.keys = {}
        if path:
            self.parse(path)

    def parse(self, path):
        self.keys = {}
        try:
            with open(path, "r") as fp:
                for line in fp:
                    line = line.strip()
                    if not line:
                        continue

                    if line.startswith("command="):
                        # TODO: This is a bit of a hack.. not sure what else could be here
                        # TODO: Do something with cmd? It'll get overwritten
                        line = line[line.find("ssh-"):]
                    l = line.split(' ')
                    cmd = None
                    if len(l) == 3:
                        keytype, key, name = l
                    else:
                        keytype, key = l
                        name = ""
                    self.keys[(keytype, key)] = name
        except IOError as exc:
            if exc.errno != 2: # No such file
                raise

    def save(self, path):
        with open(path, "w") as fp:
            fp.write(str(self))

    def includes(self, keytype, key):
        return (keytype, key) in self.keys

    def add_key(self, keytype, key, name, verify=True):
        if verify and self.includes(keytype, key):
            return False

        self.keys[(keytype, key)] = name
        return True

    def remove_key(self, keytype, key):
        try:
            self.keys.pop((keytype, key))
        except KeyError:
            return False
        return True

    def __str__(self):
        out = []
        for k, name in self.keys.items():
            keytype, key = k
            out.append(" ".join((keytype, key, name)))
        out.append("")
        return "\n".join(out)

def ssh_path_for_user(user):
    env = Environment.get_instance()
    if env.system.os == "linux":
        if user == "root":
            return "/root/.ssh/"
        return "/home/%s/.ssh/" % user
    elif env.system.platform == "mac_os_x":
        return "/Users/%s/.ssh/" % user
    raise Fail("Unable to determine ssh path for user %s on os %s platform %s" % (user, env.system.os, env.system.platform))
