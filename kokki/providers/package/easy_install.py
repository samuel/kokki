
import re
from subprocess import check_call, Popen, PIPE, STDOUT
from kokki.providers.package import PackageProvider

version_re = re.compile(r'\S\S(.*)\/(.*)-(.*)-py(.*).egg\S')
best_match_re = re.compile(r'Best match: (.*) (.*)\n')

class EasyInstallProvider(PackageProvider):
    def get_current_status(self):
        p = Popen(["python", "-c", "import %s; print %s.__path__" % (self.resource.package_name, self.resource.package_name)], stdout=PIPE, stderr=STDOUT)
        path = p.communicate()[0]
        if p.wait() != 0:
            self.current_version = None
        else:
            m = version_re.search(path)
            if m:
                self.current_version = m.group(3)
            else:
                self.current_version = "unknown"

    @property
    def candidate_version(self):
        if not hasattr(self, '_candidate_version'):
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
        return self._candidate_version

    @property
    def easy_install_binary_path(self):
        return "easy_install"

    def install_package(self, name, version):
        check_call([self.easy_install_binary_path, "-U", "%s==%s" % (name, version)], stdout=PIPE, stderr=STDOUT)

    def upgrade_package(self, name, version):
        self.install_package(name, version)

    def remove_package(self, name, version):
        check_call([self.easy_install_binary_path, "-m", name])

    def purge_package(self, name, version):
        self.remove_package(name, version)
