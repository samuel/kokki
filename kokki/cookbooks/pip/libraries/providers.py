
__all__ = ["PipPackageProvider"]

import re
from subprocess import check_call, Popen, PIPE, STDOUT
from kokki import *
from kokki.providers.package import PackageProvider


class PipPackageProvider(PackageProvider):
    def get_current_status(self):
        p = Popen("%s freeze | grep ^%s==" % (self.pip_binary_path, self.resource.package_name), stdout=PIPE, stderr=STDOUT, shell=True)
        out = p.communicate()[0]
        res = p.wait()
        if res != 0:
            self.current_version = None
        else:
            try:
                self.current_version = out.split("==", 2)[1]
            except IndexError:
                raise Fail("pip could not determine installed package version.")

    @property
    def candidate_version(self):
        if not hasattr(self, '_candidate_version'):
            if re.match("^[A-Za-z0-9_.-]+$", self.resource.package_name):
                p = Popen([self.easy_install_binary_path, "-n", self.resource.package_name], stdout=PIPE, stderr=STDOUT)
                out = p.communicate()[0]
                res = p.wait()
                if res != 0:
                    self.log.warning("easy_install check returned a non-zero result (%d) %s" % (res, self.resource))
                #     self._candidate_version = None
                # else:
                m = best_match_re.search(out)
                if not m:
                    self._candidate_version = None
                else:
                    self._candidate_version = m.group(2)
            else:
                self._candidate_vesion = self.resource.version
        return self._candidate_version

    @property
    def pip_binary_path(self):
        return "pip"

    @property
    def easy_install_binary_path(self):
        return "easy_install"

    def install_package(self, name, version):
        check_call([self.pip_binary_path, "install", name], stdout=PIPE, stderr=STDOUT)

    def update_package(self, name, version):
        self.install_package(name, version)

    def remove_package(self, name, version):
        check_call([self.pip_binary_path, "uninstall", name])

    def purge_package(self, name, version):
        self.remove_package(name, version)