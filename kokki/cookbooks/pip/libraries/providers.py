
__all__ = ["PipPackageProvider"]

from subprocess import check_call, Popen, PIPE, STDOUT
from kokki import *
from kokki.providers.package import PackageProvider


class PipInstallProvider(PackageProvider):
    def get_current_status(self):
        p = Popen([self.pip_binary_path, "freeze", "|", "grep", "^%s==" % (self.resource.package_name,)], stdout=PIPE, stderr=STDOUT, shell=True)
        out = p.communicate()[0]
        res = p.wait()
        if res != 0:
            raise Fail("pip check returned a non-zero result (%d) %s" % (res, self.resource))

        try:
            self.current_version = out.split("==", 2)[1]
        except IndexError:
            self.current_version = None

    @property
    def candidate_version(self):
        return self.resource.version

    @property
    def pip_binary_path(self):
        return "pip"

    def install_package(self, name, version):
        check_call([self.pip_binary_path, "install", name], stdout=PIPE, stderr=STDOUT)

    def update_package(self, name, version):
        self.install_package(name, version)

    def remove_package(self, name, version):
        check_call([self.pip_binary_path, "uninstall", name])

    def purge_package(self, name, version):
        self.remove_package(name, version)