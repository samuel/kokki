
from __future__ import with_statement

import os
import subprocess
from pluto.base import Fail
from pluto.providers import Provider

class FileProvider(Provider):
    def action_create(self):
        path = self.resource.path
        write = False
        content = self._get_content()
        if not os.path.exists(path):
            write = True
            reason = "it didn't exist"
        else:
            with open(path, "rb") as fp:
                old_content = fp.read()
            if content != old_content:
                write = True
                reason = "contents didn't match"

        if write:
            self.log.info("Writing %s because %s" % (self.resource, reason))
            with open(path, "wb") as fp:
                if content:
                    fp.write(content)
            self.resource.updated()

        if self.resource.mode:
            stat = os.stat(self.resource.path)
            if stat.st_mode & 0777 != self.resource.mode:
                self.log.info("Changing permission for %s from %o to %o" % (self.resource, stat.st_mode & 0777, self.resource.mode))
                os.chmod(path, self.resource.mode)
                self.resource.updated()

    def action_delete(self):
        path = self.resource.path
        if os.path.exists(path):
            self.log.info("Deleting %s" % self.resource)
            os.unlink(path)
            self.resource.updated()

    def action_touch(self):
        path = self.resource.path
        with open(path, "a") as fp:
            pass

    def _get_content(self):
        content = self.resource.content
        if isinstance(content, basestring):
            return content
        elif hasattr(content, "__call__"):
            return content()
        raise Fail("Unknown source type for %s: %r" % (self, content))


class DirectoryProvider(Provider):
    def action_create(self):
        path = self.resource.path
        if not os.path.exists(path):
            self.log.info("Creating directory %s" % self.resource)
            if self.resource.recursive:
                os.makedirs(path, self.resource.mode or 0755)
            else:
                os.mkdir(path, self.resource.mode or 0755)
            self.resource.updated()

        if self.resource.mode:
            stat = os.stat(path)
            if (stat.st_mode & 0777) != self.resource.mode:
                self.log.info("Changing permission for %s from %o to %o" % (self.resource, stat.st_mode & 0777, self.resource.mode))
                os.chmod(path, self.resource.mode)
                self.resource.updated()

    def action_delete(self):
        path = self.resource.path
        if os.path.exists(path):
            self.log.info("Removing directory %s" % self.resource)
            os.rmdir(path)
            # TODO: recursive
            self.resource.updated()


class LinkProvider(Provider):
    def action_create(self):
        path = self.resource.path
        if os.path.exists(path):
            return

        if self.resource.hard:
            self.log.info("Creating hard %s" % self.resource)
            os.link(self.resource.to, path)
            self.resource.updated()
        else:
            self.log.info("Creating symbolic %s" % self.resource)
            os.symlink(self.resource.to, path)
            self.resource.updated()

    def action_delete(self):
        path = self.resource.path
        if os.path.exists(path):
            self.log.info("Deleting %s" % self.resource)
            os.unlink(path)
            self.resource.updated()


class ExecuteProvider(Provider):
    def action_run(self):
        if self.resource.creates:
            if os.path.exists(self.resource.creates):
                return

        self.log.info("Executing %s" % self.resource)
        ret = subprocess.call(self.resource.command, shell=True, cwd=self.resource.cwd, env=self.resource.environment)
        if ret != self.resource.returns:
            raise Fail("%s failed, returned %d instead of %s" % (self, ret, self.resource.returns))
        self.resource.updated()

class ScriptProvider(Provider):
    def action_run(self):
        from tempfile import NamedTemporaryFile
        self.log.info("Running script %s" % self.resource)
        with NamedTemporaryFile(prefix="pluto-script", bufsize=0, delete=False) as tf:
            tf.write(self.resource.code)
            tf.flush()
            subprocess.call([self.resource.interpreter, tf.name], cwd=self.resource.cwd)
