
import re
from kokki.base import Fail
from kokki.providers.package import PackageProvider

class YumProvider(PackageProvider):
    def __init__(self):
        yum.YumBase.__init__(self)

    def get_current_status(self):
        #matches = self.searchGenerator(['name','version'], [self.resource.package_name])
	#for (po,matched_value) in matches:
        #    if po.name == self.resource.package_name:
        #        self.candiate_version = v
        #    else 
        #self.candidate_version = None
        pass    
    def install_package(self, name, version):
        kwargs = { "name": name, "version": version }
        self.install(None,**kwargs)

    def upgrade_package(self, name, version):
        return self.install_package(name, version)
