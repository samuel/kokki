
import re
from subprocess import check_call, Popen, PIPE, STDOUT
from pluto.providers.package import PackageProvider

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
            if p.wait() != 0:
                self.log.warning("Failed to check for python version of %s" % self.resource)
                self._candidate_version = None
            else:
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
        check_call([self.easy_install_binary_path, "%s==%s" % (name, version)], stdout=PIPE, stderr=STDOUT)

    def update_package(self, name, version):
        self.install_package(name, version)

    def remove_package(self, name, version):
        check_call([self.easy_install_binary_path, "-m", name])

    def purge_package(self, name, version):
        self.remove_package(name, version)

#            # do a dry run to get the latest version
#            command = "#{easy_install_binary_path} -n #{@new_resource.package_name}"
#            pid, stdin, stdout, stderr = popen4(command)
#            dry_run_output = ""
#            stdout.each do |line|
#              dry_run_output << line
#            end
#            dry_run_output[/(.*)Best match: (.*) (.*)\n/]
#            @candidate_version = $3
#            @candidate_version
#         end
# 
#         def install_package(name, version)
#           run_command(:command => "#{easy_install_binary_path} \"#{name}==#{version}\"")
#         end
# 
#         def upgrade_package(name, version)
#           install_package(name, version)
#         end
# 
#         def remove_package(name, version)
#           run_command(:command => "#{easy_install_binary_path} -m #{name}")
#         end
# 
#         def purge_package(name, version)
#           remove_package(name, version)
#         end
# 
#       end
#     end
#   end
# end
