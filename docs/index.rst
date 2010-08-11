=====
Kokki
=====

Kokki is a configuration management framework inspired by Chef.

Installation
============

Stable releases can be installed using::

    easy_install kokki

or::

    pip install kokki

Extra cookbooks can be found at: http://github.com/samuel/kokki-cookbooks

Source
======

You can find the latest version at http://github.com/samuel/kokki

Overview
========

In order to give us some additional, hideously cute terminology with which to
refer to the various organizational pieces of a Kokki setup, I'm (ssteinerX,
blame me) coining the term ``Kitchen`` to refer to a collection of Kokki
configuration files and associated cookbooks, recipes, providers, and
resources.

.. todo:: Make a command line utility/option to set up a new Kitchen with a
          reasonable default setup including pointing at the main Kokki cookbook
          collection and proper directory structure.

A kokki configuration is composed of a few pieces, kept in a ``Kitchen``:

*configuration file*

    specifies cookbook paths and roles.  Conventionally this is named
    ``config.yaml`` and put in the top level directory of the ``Kitchen``.

*provider*

    os/platform specific code to bring the system to the state given by a
    resource. Most of the ones you'll need are provided by the default Kokki
    installation and can be found in ``kokki/providers``.

*cookbooks*

    a collection of recipes and extra resources and providers. A pre-written
    collection of recipes is available at http://github.com/samuel/kokki-cookbooks

*recipe*

    a script that includes a various resources describing the expected state
    of a system. These are usually kept within a cookbook.

*resource*

    describes a piece of the system configuration state (e.g. described a
    file, a user, etc..).  The default Resources are in ``kokki/resources``.

    Recipe specific resources are described within the ``resources``
    directory within a recipe.

.. todo:: how to add global resources to Kokki so they can be used by multiple
          recipes without modifying kokki core?  May require new conf.yaml item?


Operation
=========

.. todo:: finish this section

    The command line is::

        kokki config_file role

    Order of operation is::

        Read config_file -- this is a .yaml file
        Read directories in `cookbook_paths:` item in config_file.yaml
        For dir in `cookbook_paths`:
            import package, run __init__.py as usual

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

cookbooks/example/recipes/web.py::

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
