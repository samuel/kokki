
from kokki import Package, Directory, Script, Fail

Package("postgresql-server-dev",
    package_name = "postgresql-server-dev-8.4")
Package("python-dev")
Package("python-psycopg2")

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

install_package("skytools",
    creates = "/usr/local/bin/pgqadm.py",
    url = "http://pgfoundry.org/frs/download.php/2370/skytools-2.1.10.tar.gz")

Directory("/etc/skytools",
    owner = "root",
    mode = 0755)
