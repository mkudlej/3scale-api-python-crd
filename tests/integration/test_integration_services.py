from tests.integration import asserts
from threescale_api.resources import Proxy, Service
from .asserts import assert_resource, assert_resource_params


def test_3scale_url_is_set(api, url, token):
    assert url is not None
    assert token is not None
    assert api.url is not None


def test_services_list(api):
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


def test_service_get_proxy(api, service: Service, proxy: Proxy):
    assert proxy['error_status_auth_failed'] == 403
    assert proxy['api_test_path'] == '/'


def test_service_set_proxy(api, service: Service, proxy: Proxy):
    updated = proxy.update(params=dict(api_test_path='/ip'))
    assert updated['error_status_auth_failed'] == 403
    assert updated['api_test_path'] == '/ip'


def test_service_proxy_promote(service, proxy, backend_usage):
    service.proxy.list().deploy()
    res = service.proxy.list().promote()
    assert res is not None
    assert res['environment'] == 'production'
    assert res['content'] is not None


def test_service_proxy_deploy(service, proxy, backend_usage, api_backend):
    # this will not propagate to proxy config but it allows deployment
    proxy.update(params=dict(api_backend=api_backend, support_email='test@example.com'))
    proxy.deploy()
    res = proxy.configs.list(env='staging')
    proxy_config = res.entity['proxy_configs'][-1]['proxy_config']
    assert proxy_config is not None
    assert proxy_config['environment'] == 'sandbox'
    assert proxy_config['content'] is not None
    assert proxy_config['version'] > 1


def test_service_list_configs(service, proxy, backend_usage):
    res = proxy.configs.list(env='staging')
    assert res
    item = res[0]
    assert item


def test_service_proxy_configs_version(service, proxy, backend_usage):
    service.proxy.list().deploy()
    config = service.proxy.list().configs.version(version=1)
    assert config
    assert config['environment'] == "sandbox"
    assert config['version'] == 1
    assert config['content']


def test_service_proxy_configs_latest(service, proxy, backend_usage):
    service.proxy.list().deploy()
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
