import pytest
import backoff

from threescale_api.errors import ApiClientError

from tests.integration import asserts

# tests important for CRD - CRU + list

def test_should_list_backend_usages(backend, service, backend_usage):
    assert len(service.backend_usages.list()) > 0
    assert len(backend.usages()) > 0

def test_should_create_backend_usage(backend_usage, backend_usage_params):
    asserts.assert_resource(backend_usage)
    asserts.assert_resource_params(backend_usage, backend_usage_params)

def test_should_read_backend_usage(backend_usage, backend_usage_params):
    resource = backend_usage.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_usage_params)

def test_should_update_backend_usage(service, backend_usage, backend_updated_usage_params):
    lcount = len(service.backend_usages.list())
    resource = backend_usage.update(params=backend_updated_usage_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_updated_usage_params)
    assert lcount == len(service.backend_usages.list())

# end of tests important for CRD - CRU + list
