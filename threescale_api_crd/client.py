import logging
import openshift as ocp
from threescale_api_crd import resources, defaults
import threescale_api

class ThreeScaleClientCRD(threescale_api.client.ThreeScaleClient):
    def __init__(self, ocp_provider_ref, *args, **kwargs):
        threescale_api.client.ThreeScaleClient.__init__(self, *args, **kwargs)
        self._ocp_provider_ref = ocp_provider_ref
        self._ocp_namespace = ocp.get_project_name()
        self._services = resources.Services(crd_client=self, instance_klass=resources.Service)

    @property
    def services(self) -> resources.Services:
        """Gets services client
        Returns(resources.Services): Services client
        """
        return self._services
    
    @property
    def ocp_provider_ref(self):
        return self._ocp_provider_ref
    
    @property
    def ocp_namespace(self):
        return self._ocp_namespace
