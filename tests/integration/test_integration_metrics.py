import pytest
import backoff

from threescale_api.errors import ApiClientError

from tests.integration import asserts


# tests important for CRD - CRU + list

def test_should_list_metrics(service, metric):
    resources = service.metrics.list()
    assert len(resources) > 0

def test_should_create_metric(metric, metric_params):
    asserts.assert_resource(metric)
    asserts.assert_resource_params(metric, metric_params)

def test_should_read_metric(metric, metric_params):
    resource = metric.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, metric_params)

def test_should_update_metric(service, metric, updated_metric_params):
    lcount = service.metrics.list()
    resource = metric.update(params=updated_metric_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, updated_metric_params)
    assert lcount == service.metrics.list()

# end of tests important for CRD - CRU + list

# TODO
#def test_should_apicast_return_403_when_metric_is_disabled(
#        service, metric_params, create_mapping_rule,
#        account, ssl_verify, backend_usage):
#    """Metric is disabled when its limit is set to 0."""
#
#    proxy = service.proxy.list()
#    plan = service.app_plans.create(params=dict(name='metrics-disabled'))
#    application_params = dict(name='metrics-disabled', plan_id=plan['id'],
#                              description='metric disabled')
#    app = account.applications.create(params=application_params)
#
#    metric = service.metrics.create(params=metric_params)
#    plan.limits(metric).create(params=dict(period='month', value=0))
#
#    rules = proxy.mapping_rules.list()
#    for rule in rules:
#        rule.delete()
#    rule = create_mapping_rule(metric, 'GET', '/foo/bah/')
#
#    update_proxy_endpoint(service, backend_usage)
#
#    # params = get_user_key_from_application(app, proxy)
#    client = app.api_client(verify=ssl_verify)
#    response = make_request(client, rule['pattern'])
#    assert response.status_code == 403
#
#
#@backoff.on_predicate(backoff.expo, lambda resp: resp.status_code == 200,
#                      max_tries=8)
#def make_request(client, path):
#    return client.get(path=path)
#
#
#def get_user_key_from_application(app, proxy):
#    user_key = app['user_key']
#    user_key_param = proxy['auth_user_key']
#    return {user_key_param: user_key}
#
#
#def update_proxy_endpoint(service, backend_usage):
#    """Update service proxy."""
#    path = backend_usage['path']
#    backend_usage['path'] = '/moloko'
#    backend_usage.update()
#    backend_usage['path'] = path
#    backend_usage.update()
#    proxy = service.proxy.list().configs.list(env='sandbox').proxy
#    proxy.deploy()
#    proxy_tmp = service.proxy.list().configs.list(env='sandbox')
#    version = proxy_tmp.entity['proxy_configs'][-1]['proxy_config']['version']
#    proxy.promote(version=version)
#
#
#def test_should_apicast_return_429_when_limits_exceeded(
#        service, application_plan, create_mapping_rule,
#        apicast_http_client, backend_usage):
#    metric_params = dict(name='limits_exceeded', unit='count',
#                         friendly_name='Limits Exceeded')
#    metric = service.metrics.create(params=metric_params)
#    limits = application_plan.limits(metric=metric)
#    limits.create(params=dict(period='day', value=1))
#
#    rule = create_mapping_rule(metric, 'GET', '/limits/exceeded/')
#
#    update_proxy_endpoint(service, backend_usage)
#
#    response = apicast_http_client.get(path=rule['pattern'])
#    while response.status_code == 200:
#        response = apicast_http_client.get(path=rule['pattern'])
#
#    assert response.status_code == 429
