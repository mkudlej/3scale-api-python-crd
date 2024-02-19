from tests.integration import asserts
from threescale_api.resources import Proxy, Service
from .asserts import assert_resource, assert_resource_params


def test_3scale_url_is_set(api, url, token):
    assert url is not None
    assert token is not None
    assert api.url is not None

# tests important for CRD - CRU + list

def test_services_list(api, service):
    services = api.services.list()
    assert len(services) >= 1

def test_service_can_be_created(api, service_params, service):
    assert_resource(service)
    assert_resource_params(service, service_params)

def test_service_can_be_read(api, service_params, service):
    read = api.services.read(service.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, service_params)


def test_service_can_be_read_by_name(api, service_params, service):
    account_name = service['system_name']
    read = api.services[account_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, service_params)

# there is different syntax for setting up backend_version
def test_service_can_be_updated(api, service):
    des_changed = (service['description'] or '') + '_changed'
    service['description'] = des_changed
    service.update()
    assert service['description'] == des_changed
    updated = service.read()
    assert updated['description'] == des_changed
    assert service['description'] == des_changed

# end of tests important for CRD - CRU + list

def test_proxy_list(api, service: Service, proxy: Proxy):
    assert not isinstance(proxy, list)

# proxy object is doesn't contain error codes until they are configured.
# there is no default value in CRD
def test_service_get_proxy(api, service: Service, proxy: Proxy):
    assert 'error_auth_failed' not in proxy.entity
    assert 'error_auth_missing' not in proxy.entity
    assert 'error_headers_auth_failed' not in proxy.entity
    assert 'error_headers_auth_missing' not in proxy.entity
    assert 'error_headers_limits_exceeded' not in proxy.entity
    assert 'error_headers_no_match' not in proxy.entity
    assert 'error_limits_exceeded' not in proxy.entity
    assert 'error_no_match' not in proxy.entity
    assert 'error_status_auth_failed' not in proxy.entity
    assert 'error_status_auth_missing' not in proxy.entity
    assert 'error_status_limits_exceeded' not in proxy.entity
    assert 'error_status_no_match' not in proxy.entity


def test_service_set_proxy(api, service: Service, proxy: Proxy):
    updated = proxy.update(params=dict(error_status_no_match=403, error_status_auth_missing=403))
    assert updated['error_status_auth_missing'] == 403
    assert updated['error_status_no_match'] == 403


def test_service_proxy_promote(service, proxy, backend_usage):
    service.proxy.list().deploy()
    service.proxy.list().promote()
    res = service.proxy.list().configs.latest(env='production')
    assert res is not None
    assert res['environment'] == 'production'
    assert res['content'] is not None


def test_service_proxy_deploy(service, proxy, backend_usage):
    proxy.update(params=dict(error_status_no_match=405, error_status_auth_missing=405))
    proxy.deploy()
    res = proxy.configs.list(env='staging')
    proxy_config = res.entity['proxy_configs'][-1]['proxy_config']
    assert proxy_config is not None
    assert proxy_config['environment'] == 'sandbox'
    assert proxy_config['content'] is not None
    assert proxy_config['version'] > 1


def test_service_list_configs(service, proxy, backend_usage):
    proxy.update(params=dict(error_status_no_match=406, error_status_auth_missing=406))
    proxy.deploy()
    res = proxy.configs.list(env='staging')
    assert res
    item = res[0]
    assert item


def test_service_proxy_configs_version(service, proxy, backend_usage):
    config = service.proxy.list().configs.version(version=1)
    assert config
    assert config['environment'] == "sandbox"
    assert config['version'] == 1
    assert config['content']


def test_service_proxy_configs_latest(service, proxy, backend_usage):
    config = service.proxy.list().configs.latest()
    assert config
    assert config['environment'] == "sandbox"
    assert config['version']
    assert config['content']


def test_service_proxy_configs_list_length(service, proxy, backend_usage, api_backend):
    configs = service.proxy.list().configs.list(env="sandbox")
    length = len(configs)
    proxy.update(params=dict(error_status_auth_failed=417, api_backend=api_backend))
    configs = service.proxy.list().configs.list(env="sandbox")
    assert len(configs) == length + 1

# there is no default mapping rule in service created from CRD
def test_service_mapping_rules(service):
    map_rules = service.mapping_rules.list()
    assert len(map_rules) == 0 


def test_service_backend_usages_backend(backend_usage, backend):
    assert backend_usage.backend.entity_id == backend.entity_id


def test_service_active_docs(service, active_doc):
    assert all([acs['service_id'] == service['id'] for acs in service.active_docs.list()])
