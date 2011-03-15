
import os
from kokki import Package, File, Template, Service

Service("postgresql-9.0",
    supports_restart = True,
    supports_reload = True,
    supports_status = True,
    action = "nothing")

Package("postgresql-9.0",
    notifies = [("stop", env.resources["Service"]["postgresql-9.0"], True)])

File("pg_hba.conf",
    owner = "postgres",
    group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql9.config_dir, "pg_hba.conf"),
    content = Template("postgresql9/pg_hba.conf.j2"),
    notifies = [("reload", env.resources["Service"]["postgresql-9.0"])])

File("postgresql.conf",
    owner = "postgres",
    group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql9.config_dir, "postgresql.conf"),
    content = Template("postgresql9/postgresql.conf.j2"),
    notifies = [("restart", env.resources["Service"]["postgresql-9.0"])])
