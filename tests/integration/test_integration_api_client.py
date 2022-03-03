from threescale_api.utils import HttpClient


def test_api_client(service):
    api_client = service.threescale_client
    api_client.rest._ssl_verify = False

    assert api_client is not None
    assert api_client.services.list()

    assert api_client.ocp_provider_ref
    assert api_client.ocp_namespace
    assert service.crd
