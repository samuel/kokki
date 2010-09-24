
from __future__ import with_statement

import grp
import os
import pwd
import subprocess
from kokki.base import Fail
from kokki.providers import Provider

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

        stat = os.stat(self.resource.path)

        if self.resource.mode:
            if stat.st_mode & 07777 != self.resource.mode:
                self.log.info("Changing permission for %s from %o to %o" % (self.resource, stat.st_mode & 07777, self.resource.mode))
                os.chmod(path, self.resource.mode)
                self.resource.updated()

        if self.resource.owner:
            try:
                new_uid = int(self.resource.owner)
            except ValueError:
                new_uid = pwd.getpwnam(self.resource.owner).pw_uid
            if stat.st_uid != new_uid:
                self.log.info("Changing owner for %s from %d to %s" % (self.resource, stat.st_uid, self.resource.owner))
                os.chown(path, new_uid, -1)

        if self.resource.group:
            try:
                new_gid = int(self.resource.group)
            except ValueError:
                new_gid = grp.getgrnam(self.resource.group).gr_gid 
            if stat.st_gid != new_gid:
                self.log.info("Changing group for %s from %d to %s" % (self.resource, stat.st_gid, self.resource.group))
                os.chown(path, -1, new_gid)

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

        stat = os.stat(path)
        if self.resource.mode:
            if (stat.st_mode & 07777) != self.resource.mode:
                self.log.info("Changing permission for %s from %o to %o" % (self.resource, stat.st_mode & 07777, self.resource.mode))
                os.chmod(path, self.resource.mode)
                self.resource.updated()

        if self.resource.owner:
            try:
                new_uid = int(self.resource.owner)
            except ValueError:
                new_uid = pwd.getpwnam(self.resource.owner).pw_uid
            if stat.st_uid != new_uid:
                self.log.info("Changing owner for %s from %d to %s" % (self.resource, stat.st_uid, self.resource.owner))
                os.chown(path, new_uid, -1)

        if self.resource.group:
            try:
                new_gid = int(self.resource.group)
            except ValueError:
                new_gid = grp.getgrnam(self.resource.group).gr_gid 
            if stat.st_gid != new_gid:
                self.log.info("Changing group for %s from %d to %s" % (self.resource, stat.st_gid, self.resource.group))
                os.chown(path, -1, new_gid)

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
            oldpath = os.path.realpath(path)
            if oldpath == self.resource.to:
                return
            if not os.path.islink(path):
                raise Fail("%s trying to create a symlink with the same name as an existing file or directory" % self)
            self.log.info("%s replacing old symlink to %s" % (self, oldpath))
            os.unlink(path)

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
        with NamedTemporaryFile(prefix="kokki-script", bufsize=0) as tf:
            tf.write(self.resource.code)
            tf.flush()
            subprocess.call([self.resource.interpreter, tf.name], cwd=self.resource.cwd)
