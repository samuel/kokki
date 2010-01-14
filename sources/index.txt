=====
Kokki
=====

Kokki is a configuration management framework inspired by Chef.

Installation
============

Stable releases can be installed using
``easy_install`` or ``pip``.

Extra cookbooks can be found at:
http://github.com/samuel/kokki-cookbooks

Source
======

You can find the latest version at
http://github.com/samuel/kokki

Overview
========

A kokki configuration is composed of a few pieces:

*configuration file*
    specifies cookbook paths and roles
*cookbooks*
    a collection of recipes and extra resources and providers
*recipe*
    a script that includes a various resources describing the expected state of a system
*resource*
    describes a piece of the system configuration state (e.g. described a file, a user, etc..)
*provider*
    os/platform specific code to bring the system to the state given by a resource

Example
=======

config.yaml::

    cookbook_paths: [cookbooks]
    roles:
        base:
            description: Base role for all systems
            recipes: [example]
            default_attributes:
                example.web_port: 80
        web:
            description: Web node
            parents: [base]
            recipes: [example.web]
            override_attributes:
                example.web_port: 8080

cookbooks/example/__init__.py::

    # [empty]

cookbooks/example/metadata.yaml::

    description: Example cookbook
    attributes:
        example.web_port:
            display_name: Web port to listen on
            description: Port number on which Apache should listen for new connections
            default: 80

cookbooks/example/recipes/default.py::

    from kokki import *

    Package("git-core")

cookbooks/example/recipes/::

    from kokki import *

    Package("apache2")
    File("/etc/apache2/ports.conf",
        owner = "www-data",
        content = "Listen %d\n" % env.example.web_port)

To run the 'web' role on the local system::

    kokki config.yaml web
    or
    python -m kokki.runner config.yaml web

TOC
===

.. toctree::
   :maxdepth: 2

   resources
