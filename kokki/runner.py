
from __future__ import with_statement

__all__ = ["Kokki"]

import logging
import os
import yaml
from kokki import register_cookbook_path, load_cookbook, include_recipe, find_provider
from kokki import env as global_env

class Kokki(object):
    def __init__(self, config):
        if isinstance(config, basestring):
            with open(config, "rb") as fp:
                config = yaml.load(fp.read())

        self.log = logging.getLogger("kokki")
        self.config = config
        self.env = global_env

        self.cookbooks = []
        for path in self.config['cookbook_paths']:
            register_cookbook_path(path)
            for cb in os.listdir(path):
                self.cookbooks.append((cb, path))

    def load_cookbooks(self):
        for cb, path in self.cookbooks:
            load_cookbook(cb, path)

    def run_action(self, resource, action):
        self.log.debug("Performing action %s on %s" % (action, resource))

        provider_class = find_provider(resource.__class__.__name__, resource.provider)
        provider = provider_class(resource)
        getattr(provider, 'action_%s' % action)()

        if resource.is_updated:
            for action, res in resource.subscriptions['immediate']:
                self.log.info("%s sending %s action to %s (immediate)" % (resource, action, res))
                self.run_action(res, action)
            for action, res in resource.subscriptions['delayed']:
                self.log.info("%s sending %s action to %s (delayed)" % (resource, action, res))
            self.delayed_actions |= resource.subscriptions['delayed']

    def _check_condition(self, cond):
        if hasattr(cond, '__call__'):
            return cond()

        if isinstance(cond, basestring):
            import subprocess
            ret = subprocess.call(cond, shell=True)
            return ret == 0

        raise Exception("Unknown condition type %r" % cond)

    def run_roles(self, roles):
        self.env.reset()
        self.delayed_actions = set()

        # Make a full list of roles including parents
        full_roles = []
        def add_roles(roles):
            for name in roles:
                if name in full_roles:
                    continue

                role = self.config['roles'][name]
                if 'parents' in role:
                    add_roles(role['parents'])

                if name not in full_roles:
                    full_roles.append(name)
        add_roles(roles)

        # Find roles and set default attributes
        _roles = []
        for name in full_roles:
            role = self.config['roles'][name]
            self.env.set_attributes(role.get('default_attributes') or {}, overwrite=False)
            _roles.append(role)

        # Load all cookbooks so they can setup the environment
        self.load_cookbooks()

        # Override attributes for all roles
        for role in _roles:
            self.env.set_attributes(role.get('override_attributes') or {}, overwrite=True)

        # Run recipes for all roles
        for role in _roles:
            for recipe in role['recipes']:
                include_recipe(recipe)

        # Run resource actions
        for resource in self.env.resource_list:
            if resource.not_if is not None and self._check_condition(resource.not_if):
                self.log.debug("Skipping %s due to not_if" % resource)
                continue

            if resource.only_if is not None and not self._check_condition(resource.only_if):
                self.log.debug("Skipping %s due to only_if" % resource)
                continue

            for action in resource.action:
                self.run_action(resource, action)

        # Run delayed actions
        for action, resource in self.delayed_actions:
            self.run_action(resource, action)

def main():
    import logging
    import sys

    config = sys.argv[1]
    roles = sys.argv[2:]

    logging.basicConfig(level=logging.INFO)

    kokki = Kokki(config)
    kokki.run_roles(roles)

if __name__ == "__main__":
    main()
