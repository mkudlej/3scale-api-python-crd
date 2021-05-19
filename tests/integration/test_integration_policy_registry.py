from tests.integration import asserts
from threescale_api.resources import PolicyRegistry
from .asserts import assert_resource, assert_resource_params


# tests important for CRD - CRU + list

def test_policy_registry_list(api, policy_registry):
    objs = api.policy_registry.list()
    assert len(objs) >= 1

def test_policy_registry_can_be_created(api, policy_registry_params, policy_registry):
    assert_resource(policy_registry)
    assert_resource_params(policy_registry, policy_registry_params)

def test_policy_registry_can_be_read(api, policy_registry_params, policy_registry):
    read = api.policy_registry.read(policy_registry.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, policy_registry)


def test_policy_regitry_can_be_read_by_name(api, policy_registry_params, policy_registry):
    name = policy_registry['name']
    read = api.policy_registry[name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, policy_registry)

def test_policy_registry_can_be_updated(api, service, policy_registry):
    des_changed = (policy_registry['name'] or '') + '_changed'
    policy_registry['name'] = des_changed
    policy_registry.update()
    assert policy_registry['name'] == des_changed
    updated = policy_registry.read()
    assert updated['name'] == des_changed
    assert policy_registry['name'] == des_changed

# end of tests important for CRD - CRU + list

# tests to compare data in CRD and in 3scale

def test_data(api, api_origin, policy_registry):
    for pol in api.policy_registry.list():
        pol_origin = api_origin.policy_registry.read(int(pol['id']))
        for att in pol.entity:
             assert pol.entity[att] == pol_origin.entity[att]
