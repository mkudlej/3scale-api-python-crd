import pytest

from tests.integration import asserts


# tests important for CRD - CRU + list

def test_should_list_mapping_rules(backend, backend_mapping_rule):
    resource = backend.mapping_rules.list()
    assert resource

def test_should_create_mapping_rule(backend_mapping_rule, backend_mapping_rule_params):
    asserts.assert_resource(backend_mapping_rule)
    asserts.assert_resource_params(backend_mapping_rule, backend_mapping_rule_params)

def test_should_read_mapping_rule(backend_mapping_rule, backend_mapping_rule_params):
    resource = backend_mapping_rule.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_mapping_rule_params)

def test_should_update_mapping_rule(service, backend, backend_usage,
        updated_backend_mapping_rules_params, application, apicast_http_client):
    resource = backend.mapping_rules.create(updated_backend_mapping_rules_params)
    pattern = '/anything/test-foo'
    resource['pattern'] = pattern
    resource.update()
    updated_resource = resource.read()
    assert updated_resource['pattern'] == pattern

    service.proxy.deploy()

    response = apicast_http_client.get(path=f"{backend_usage['path']}{pattern}")
    asserts.assert_http_ok(response)

# end of tests important for CRD - CRU + list


def test_should_mapping_rule_endpoint_return_ok(service, backend,
        backend_mapping_rule, backend_usage, application, apicast_http_client):
    service.proxy.deploy()

    response = apicast_http_client.get(path=f"{backend_usage['path']}{backend_mapping_rule['pattern']}")
    asserts.assert_http_ok(response)


def test_stop_processing_mapping_rules_once_first_one_is_met(service,
        backend_usage, backend, updated_backend_mapping_rules_params, application,
        apicast_http_client):
    params_first = updated_backend_mapping_rules_params.copy()
    params_first['pattern'] = '/anything/search'
    resource_first = backend.mapping_rules.create(params=params_first)
    assert resource_first.exists()

    params_second = updated_backend_mapping_rules_params.copy()
    params_second['pattern'] = '/anything/{id}'
    resource_second = backend.mapping_rules.create(params=params_second)
    assert resource_second.exists()

    service.proxy.deploy()

    response = apicast_http_client.get(path=f"{backend_usage['path']}{params_first['pattern']}")
    asserts.assert_http_ok(response)

    assert params_first['pattern'] in response.url
