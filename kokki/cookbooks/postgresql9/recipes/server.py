
import os
from kokki import Package, File, Template, Service

env.include_recipe("postgresql9")

Service("postgresql",
    supports_restart = True,
    supports_reload = True,
    supports_status = True,
    action = "nothing")

Package("postgresql-9.0",
    notifies = [("stop", env.resources["Service"]["postgresql"], True)])

File("pg_hba.conf",
    owner = "postgres",
    group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql9.config_dir, "pg_hba.conf"),
    content = Template("postgresql9/pg_hba.conf.j2"),
    notifies = [("reload", env.resources["Service"]["postgresql"])])

File("postgresql.conf",
    owner = "postgres",
    group = "postgres",
    mode = 0600,
    path = os.path.join(env.config.postgresql9.config_dir, "postgresql.conf"),
    content = Template("postgresql9/postgresql.conf.j2"),
    notifies = [("restart", env.resources["Service"]["postgresql"])])
