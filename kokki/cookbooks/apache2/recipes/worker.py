
from kokki import Package

env.include_recipe("apache2")

Package("apache2-mpm-worker")
