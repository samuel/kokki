
import os
from kokki import Service, File, Package, Template

Service("postgresql",
    supports_restart = True,
    supports_reload = True,
    supports_status = True,
    action = "nothing")

Package("postgresql-8.4",
    notifies = [("stop", env.resources["Service"]["postgresql"], True)])

File("pg_hba.conf",
    owner = "postgres",
    group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql84.config_dir, "pg_hba.conf"),
    content = Template("postgresql84/pg_hba.conf.j2"),
    notifies = [("reload", env.resources["Service"]["postgresql"])])

File("postgresql.conf",
    owner = "postgres",
    group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql84.config_dir, "postgresql.conf"),
    content = Template("postgresql84/postgresql.conf.j2"),
    notifies = [("restart", env.resources["Service"]["postgresql"])])
