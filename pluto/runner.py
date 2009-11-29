
from __future__ import with_statement

__all__ = ["Pluto"]

import logging
import os
import yaml
from pluto import register_cookbook_path, load_cookbook, include_recipe, find_provider
from pluto import env as global_env

class Pluto(object):
    def __init__(self, config):
        if isinstance(config, basestring):
            with open(config, "rb") as fp:
                config = yaml.load(fp.read())

        self.log = logging.getLogger("pluto")
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

    def run_role(self, role):
        for recipe in role['recipes']:
            include_recipe(recipe)

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

    def run_roles(self, roles):
        self.env.reset()
        self.delayed_actions = set()
        _roles = []
        for name in roles:
            role = self.config['roles'][name]
            self.env.set_attributes(role.get('default_attributes') or {}, overwrite=False)
            _roles.append(role)
        self.load_cookbooks()
        for role in _roles:
            self.env.set_attributes(role.get('override_attributes') or {}, overwrite=True)
            self.run_role(role)
