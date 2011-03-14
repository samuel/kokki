
import os
from kokki import Package, Script, User, Directory, File, Template, Execute, Fail, Service

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

Package("build-essential")
Package("bison")
Package("flex")
Package("libreadline-dev")
Package("zlib1g-dev")

options = []
if env.config.postgresql9.with_openssl:
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
    env.config.postgresql9.root_dir,
    options)

User("postgres",
    home = env.config.postgresql9.root_dir,
    system = True)

Directory(env.config.postgresql9.root_dir,
    owner = "postgres")

File("%s/.profile" % env.config.postgresql9.root_dir,
    owner = "postgres",
    content = "#!/bin/sh\nexport PATH=%s/bin:$PATH\n" % env.config.postgresql9.root_dir)

Execute("sudo -u postgres -i initdb %s" % env.config.postgresql9.data_dir,
    creates = "%s/base" % env.config.postgresql9.data_dir)

Service("postgresql",
    start_command = "sudo -u postgres -i pg_ctl start -w -D {postgresql9.data_dir} -l {postgresql9.data_dir}/postgresql.log".format(postgresql9=env.config.postgresql9),
    stop_command = "sudo -u postgres -i pg_ctl stop -w -D {postgresql9.data_dir} -m smart".format(postgresql9=env.config.postgresql9),
    restart_command = "sudo -u postgres -i pg_ctl restart -w -D {postgresql9.data_dir} -m smart".format(postgresql9=env.config.postgresql9),
    reload_command = "sudo -u postgres -i pg_ctl reload -D {postgresql9.data_dir}".format(postgresql9=env.config.postgresql9),
    status_command = "sudo -u postgres -i pg_ctl status -D {postgresql9.data_dir}".format(postgresql9=env.config.postgresql9),
    action = "nothing")

File("pg_hba.conf",
    owner = "postgres",
    # group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql9.config_dir, "pg_hba.conf"),
    content = Template("postgresql9/pg_hba.conf.j2"),
    notifies = [("reload", env.resources["Service"]["postgresql"])])

File("postgresql.conf",
    owner = "postgres",
    # group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql9.config_dir, "postgresql.conf"),
    content = Template("postgresql9/postgresql.conf.j2"),
    notifies = [("restart", env.resources["Service"]["postgresql"])])
