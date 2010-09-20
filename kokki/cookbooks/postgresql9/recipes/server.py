
import os
from kokki import *

def install_package(name, url, creates, options=None):
    import os
    filename = url.rsplit('/', 1)[-1]
    dirname = filename
    while dirname.rsplit('.', 1)[-1] in ('gz', 'tar', 'tgz', 'bz2'):
        dirname = dirname.rsplit('.', 1)[0]

    if not dirname:
        raise Fail("Unable to figure out directory name of project for URL %s" % url)

    options = " ".join(options) if options else ""

    Script("install-%s" % name,
        not_if = lambda:os.path.exists(creates),
        cwd = "/usr/local/src",
        code = (
            "wget %(url)s\n"
            "tar -zxvf %(filename)s\n"
            "cd %(dirname)s\n"
            "./configure %(options)s && make install\n"
            "ldconfig\n") % dict(url=url, dirname=dirname, filename=filename, options=options)
    )

Package("bison")
Package("flex")
Package("libreadline-dev")
Package("zlib1g-dev")

options = []
if env.config.postgresql9.with_ssl:
    Package("libssl-dev")
    options.append("--with-openssl")
if env.config.postgresql9.with_xml:
    Package("libxml2-dev")
    options.append("--with-libxml")
if env.config.postgresql9.with_perl:
    Package("libperl-dev")
    options.append("--with-perl")
if env.config.postgresql9.with_python:
    Package("python-dev")
    options.append("--with-python")

install_package("postgresql9",
    env.config.postgresql9.package_url,
    "/usr/local/pgsql",
    options)
