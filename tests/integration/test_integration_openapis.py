import json

from tests.integration import asserts
from .asserts import assert_resource, assert_resource_params

# tests important for CRD - CRU + list

def test_openapis_list(api, openapi):
    openapis = api.openapis.list()
    assert len(openapis) >= 1

def test_openapi_can_be_created(api, openapi_params, openapi):
    assert_resource(openapi)
    assert_resource_params(openapi, openapi_params)

def test_openapi_can_be_read(api, openapi_params, openapi):
    read = api.openapis.read(openapi.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, openapi_params)


def test_openapi_can_be_updated(api, openapi):
    des_changed = (openapi['productSystemName'] or '') + '_changed'
    openapi['productSystemName'] = des_changed
    openapi.update()
    assert openapi['productSystemName'] == des_changed
    updated = openapi.read()
    assert updated['productSystemName'] == des_changed
    assert openapi['productSystemName'] == des_changed

# end of tests important for CRD - CRU + list
