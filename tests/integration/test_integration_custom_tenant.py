from tests.integration import asserts
from .asserts import assert_resource, assert_resource_params


def test_3scale_master_url_is_set(master_api, master_url, master_token):
    assert master_url
    assert master_token
    assert master_api.url


# tests important for CRD - CRU + list


def test_tenants_list(api, custom_tenant):
    tenants = api.tenants.list()
    assert len(tenants) >= 1


def test_tenant_can_be_created(custom_tenant, tenant_params):
    asserts.assert_resource(custom_tenant)
    assert custom_tenant.entity["signup"]["account"]["admin_base_url"]
    assert custom_tenant.entity["signup"]["access_token"]["value"]


def test_tenant_can_be_read(api, tenant_params, custom_tenant):
    read = api.tenants.read(custom_tenant.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, tenant_params)


# this test does not make sense in 3scale api client too
#   def test_tenant_can_be_read_by_name(api, tenant_params, custom_tenant):
#       tenant_name = custom_tenant['name']
#       read = api.tenants[tenant_name]
#       asserts.assert_resource(read)
#       asserts.assert_resource_params(read, tenant_params)


def test_tenant_can_be_updated(api, custom_tenant):
    des_changed = (custom_tenant["signup"]["account"]["email"] or "") + "_changed"
    custom_tenant["signup"]["account"]["email"] = des_changed
    custom_tenant.update()
    assert custom_tenant["signup"]["account"]["email"] == des_changed
    updated = custom_tenant.threescale_client.tenants.read(custom_tenant.entity_id)
    assert updated["signup"]["account"]["email"] == des_changed
    assert custom_tenant["signup"]["account"]["email"] == des_changed


# end of tests important for CRD - CRU + list
