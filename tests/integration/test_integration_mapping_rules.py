import pytest
import requests

from tests.integration import asserts


# tests important for CRD - CRU + list


def test_should_list_mapping_rules(proxy, mapping_rule):
    resource = proxy.mapping_rules.list()
    # there is not default mapping rule in CRD
    assert len(resource) > 0


def test_should_create_mapping_rule(mapping_rule, mapping_rule_params):
    asserts.assert_resource(mapping_rule)
    asserts.assert_resource_params(mapping_rule, mapping_rule_params)


def test_should_read_mapping_rule(mapping_rule, mapping_rule_params):
    resource = mapping_rule.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, mapping_rule_params)


def test_should_update_mapping_rule(
    service,
    backend,
    mapping_rule,
    updated_mapping_rules_params,
    backend_usage,
    application,
    apicast_http_client,
):
    resource = service.mapping_rules.create(params=updated_mapping_rules_params)
    lcount = service.mapping_rules.list()
    delta = 11
    resource["delta"] = delta
    resource.update()
    updated_resource = resource.read()
    assert updated_resource["delta"] == delta
    assert len(lcount) == len(service.mapping_rules.list())
    service.proxy.deploy()
    response = apicast_http_client.get(path=resource["pattern"])
    asserts.assert_http_ok(response)


# end of tests important for CRD - CRU + list


def test_should_mapping_rule_endpoint_return_ok(
    mapping_rule, backend_usage, apicast_http_client, application, application_plan
):
    response = apicast_http_client.get(path=mapping_rule["pattern"])
    asserts.assert_http_ok(response)


def test_stop_processing_mapping_rules_once_first_one_is_met(
    proxy,
    updated_mapping_rules_params,
    backend_usage,
    apicast_http_client,
    application,
    application_plan,
):
    params_first = updated_mapping_rules_params.copy()
    params_first["pattern"] = "/anything/search"
    resource_first = proxy.mapping_rules.create(params=params_first)
    assert resource_first.exists()

    params_second = updated_mapping_rules_params.copy()
    params_second["pattern"] = "/anything/{id}"
    resource_second = proxy.mapping_rules.create(params=params_second)
    assert resource_second.exists()

    proxy.deploy()
    response = apicast_http_client.get(path=params_first["pattern"])
    asserts.assert_http_ok(response)

    assert params_first["pattern"] in response.url
