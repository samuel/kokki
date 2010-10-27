
__description__ = """
This project is a repository of simple utilities written in various scripting
languages, which are designed to make slow tasks a bit faster. The name is
taken from the common garden snail. Many of these tools are developed by
consultants at Percona, where the author works.

http://code.google.com/p/aspersa/
"""
__config__ = {
    "aspersa.install_path": dict(
        description = "Path where to install the scripts",
        default = "/usr/local/bin",
    ),
    "aspersa.scripts": dict(
        description = "List of scripts to install",
        default = [
            "align", "collect", "diskstats", "iodump", "ioprofile", "mext",
            "mext2", "mysql-summary", "pmp", "rel", "sif", "slowlog",
            "snoop-to-tcpdump", "stalk", "summary", "usl",
        ],
    ),
}
