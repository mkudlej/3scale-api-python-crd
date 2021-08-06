"""
Module with ThreeScaleClient for CRD.
"""

import logging
import openshift as ocp
from threescale_api_crd import resources, defaults
import threescale_api

class ThreeScaleClientCRD(threescale_api.client.ThreeScaleClient):
    """
    Threescale client for CRD.
    """
    def __init__(self, ocp_provider_ref, *args, **kwargs):
        threescale_api.client.ThreeScaleClient.__init__(self, *args, **kwargs)
        self._ocp_provider_ref = ocp_provider_ref
        self._ocp_namespace = ocp.get_project_name()
        self._services = resources.Services(crd_client=self, instance_klass=resources.Service)
        self._active_docs = resources.ActiveDocs(
            crd_client=self,
            instance_klass=resources.ActiveDoc)
        self._policy_registry = resources.PoliciesRegistry(
            self,
            instance_klass=resources.PolicyRegistry)
        self._backends = resources.Backends(crd_client=self, instance_klass=resources.Backend)
        self._accounts = resources.Accounts(self, instance_klass=resources.Account)
        self._accounts_users = resources.AccountUsers(self, instance_klass=resources.AccountUser)
        self._openapis = resources.OpenApis(self, instance_klass=resources.OpenApi)

    @property
    def services(self) -> resources.Services:
        """Gets services client
        Returns(resources.Services): Services client
        """
        return self._services

    @property
    def active_docs(self) -> resources.ActiveDocs:
        """Gets active docs client
        Returns(resources.ActiveDocs): ActiveDocs client
        """
        return self._active_docs

    @property
    def policy_registry(self) -> resources.PolicyRegistry:
        """Gets policy registry client
        Returns(resources.PolicyRegistry): Policy Registry client
        """
        return self._policy_registry

    @property
    def backends(self) -> resources.Backend:
        """Gets backend client
        Returns(resources.Backend): Backend client
        """
        return self._backends
    
    @property
    def accounts(self) -> resources.Accounts:
        """Gets accounts client
        Returns(resources.Accounts): Accounts client
        """
        return self._accounts

    @property
    def account_users(self) -> resources.AccountUsers:
        """Gets account users client
        Returns(resources.AccountUsers): Account Users client
        """
        return self._accounts_users
    
    @property
    def open_apis(self) -> resources.OpenApis:
        """Gets AopenApis client
        Returns(resources.OpenApis): OpenApis client
        """
        return self._openapis

    @property
    def ocp_provider_ref(self):
        """Gets provider reference """
        return self._ocp_provider_ref

    @property
    def ocp_namespace(self):
        """Gets working namespace"""
        return self._ocp_namespace
