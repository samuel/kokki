
from kokki import Package, Directory, Script, Template, Fail

env.include_recipe("monit")

def install_package(name, url, creates):
    import os
    filename = url.rsplit('/', 1)[-1]
    dirname = filename
    while dirname.rsplit('.', 1)[-1] in ('gz', 'tar', 'tgz', 'bz2'):
        dirname = dirname.rsplit('.', 1)[0]

    if not dirname:
        raise Fail("Unable to figure out directory name of project for URL %s" % url)

    Script("install-%s" % name,
        not_if = lambda:os.path.exists(creates),
        cwd = "/usr/local/src",
        code = (
            "wget %(url)s\n"
            "tar -zxvf %(filename)s\n"
            "cd %(dirname)s\n"
            "./configure && make install\n"
            "ldconfig\n") % dict(url=url, dirname=dirname, filename=filename)
    )

Package("uuid-dev")
Package("libevent-dev")
Package("g++")
install_package("gearmand",
    creates = "/usr/local/sbin/gearmand",
    url = "http://launchpad.net/gearmand/trunk/0.14/+download/gearmand-0.14.tar.gz")

Directory("/var/run/gearmand",
    owner = "nobody",
    mode = 0755)
env.cookbooks.monit.rc("gearmand",
    content = Template("gearmand/monit.conf.j2"))
