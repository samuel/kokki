
from kokki import env, Package

env.include_recipe("zookeeper")

Package("hadoop-zookeeper-server")
