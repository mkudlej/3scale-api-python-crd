import pytest

import openshift_client as ocp
from openshift_client import OpenShiftPythonException
from threescale_api_crd import client


@pytest.fixture()
def url():
    return 'http://localhost'


@pytest.fixture()
def token():
    return 'test-token'

@pytest.fixture(scope='session')
def ocp_provider_ref() -> str:
    return 'secret'


def _create_client(url, token, ocp_provider_ref, **kwargs) -> client.ThreeScaleClientCRD:
    return client.ThreeScaleClientCRD(url=url, token=token, ocp_provider_ref=ocp_provider_ref, **kwargs)


@pytest.fixture()
def api(url, token, ocp_provider_ref):
    return _create_client(url, token, ocp_provider_ref)

@pytest.fixture()
def namespace():
    try:
        return ocp.get_project_name()
    except OpenShiftPythonException:
        return "NOT LOGGED IN"


@pytest.mark.smoke
def test_api_client_initialization(api, url, ocp_provider_ref, namespace):
    assert api.url == url
    assert api.parent == api
    assert api.threescale_client == api
    assert api.admin_api_url == f'{url}/admin/api'
    assert api.ocp_provider_ref == ocp_provider_ref
    assert api.ocp_namespace == namespace
