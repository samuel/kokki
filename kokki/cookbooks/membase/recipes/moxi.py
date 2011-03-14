
if env.system.platform in ("ubuntu", "debian"):
    if env.system.arch == "x86_64":
        deb_url = "http://c2493362.cdn.cloudfiles.rackspacecloud.com/moxi-server_x86_64_1.6.0.deb"
    elif env.system.arch == "x86_32":
        deb_url = "http://c2493362.cdn.cloudfiles.rackspacecloud.com/moxi-server_x86_1.6.0.deb"
    # TODO: Install deb
elif env.system.platform in ("fedora", "redhat"):
    if env.system.arch == "x86_64":
        rpm_url = "http://c2493362.cdn.cloudfiles.rackspacecloud.com/moxi-server_x86_64_1.6.0.rpm"
    elif env.system.arch == "x86_32":
        rpm_url = "http://c2493362.cdn.cloudfiles.rackspacecloud.com/moxi-server_x86_1.6.0.rpm"
    # TODO: Install rpm
