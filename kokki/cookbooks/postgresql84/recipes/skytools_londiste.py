
from kokki import *

env.include_recipe("postgresql84.skytools")

File("/etc/skytools/londiste.ini",
    owner = "root",
    content = Template("postgresql84/skytools-londiste.ini.j2"))
