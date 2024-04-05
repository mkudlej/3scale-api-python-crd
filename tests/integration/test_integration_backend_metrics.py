import pytest
import backoff

from threescale_api.errors import ApiClientError

from tests.integration import asserts

# tests important for CRD - CRU + list


def test_should_list_metrics(backend, backend_metric):
    resources = backend.metrics.list()
    assert len(resources) > 0


def test_should_create_metric(backend_metric, backend_metric_params):
    asserts.assert_resource(backend_metric)
    asserts.assert_resource_params(backend_metric, backend_metric_params)


def test_should_read_metric(backend_metric, backend_metric_params):
    resource = backend_metric.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_metric_params)


def test_should_update_metric(
    backend, backend_metric, backend_metric_params, backend_updated_metric_params
):
    lcount = len(backend.metrics.list())
    resource = backend_metric.update(params=backend_updated_metric_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_updated_metric_params)
    assert lcount == len(backend.metrics.list())


# end of tests important for CRD - CRU + list

# def test_should_fields_be_required(backend):
#    resource = backend.metrics.create(params={}, throws=False)
#    asserts.assert_errors_contains(resource, ['friendly_name', 'unit'])


# def test_should_system_name_be_invalid(backend, backend_metric_params):
#    backend_metric_params['system_name'] = 'invalid name whitespaces'
#    resource = backend.metrics.create(params=backend_metric_params, throws=False)
#    asserts.assert_errors_contains(resource, ['system_name'])


# def test_should_raise_exception(backend):
#    with pytest.raises(ApiClientError):
#        backend.metrics.create(params={})


def test_should_apicast_return_403_when_metric_is_disabled(
    service,
    backend,
    backend_usage,
    backend_metric_params,
    application_plan,
    application,
    apicast_http_client,
):
    """Metric is disabled when its limit is set to 0."""

    bmetric_params = backend_metric_params.copy()
    bmetric_params["friendly_name"] += "403"
    back_metric = backend.metrics.create(params=bmetric_params)

    mapping_params = dict(
        http_method="GET",
        pattern="/anything/post/id",
        metric_id=back_metric["id"],
        delta=1,
    )
    back_mapping = backend.mapping_rules.create(params=mapping_params)

    limits = application_plan.limits(back_metric)
    back_lim = limits.create(params=dict(period="month", value=0))

    proxy = service.proxy.list()
    proxy.deploy()

    response = apicast_http_client.get(path=f"{back_mapping['pattern']}")
    assert response.status_code == 403
    back_lim.delete()
    back_mapping.delete()
    proxy.deploy()
    back_metric.delete()


@backoff.on_predicate(backoff.expo, lambda resp: resp.status_code == 200, max_tries=8)
def make_request(client, path):
    return client.get(path=path)


def get_user_key_from_application(app, proxy):
    user_key = app["user_key"]
    user_key_param = proxy["auth_user_key"]
    return {user_key_param: user_key}


def test_should_apicast_return_429_when_limits_exceeded(
    service, backend, backend_usage, application_plan, application, apicast_http_client
):
    metric_params = dict(
        name="limits_exceeded", unit="count", friendly_name="Limits Exceeded"
    )
    back_metric = backend.metrics.create(params=metric_params)

    mapping_params = dict(
        http_method="GET",
        pattern="/anything/limits/exceeded",
        metric_id=back_metric["id"],
        delta=1,
    )
    back_mapping = backend.mapping_rules.create(params=mapping_params)

    back_lim = application_plan.limits(back_metric).create(
        params=dict(period="day", value=1)
    )

    proxy = service.proxy.list()
    proxy.deploy()

    response = apicast_http_client.get(path=f"{back_mapping['pattern']}")
    while response.status_code == 200:
        response = apicast_http_client.get(path=f"{back_mapping['pattern']}")

    assert response.status_code == 429
    back_lim.delete()
    back_mapping.delete()
    proxy.deploy()
    back_metric.delete()


# def test_should_remove_limits_and_pricings_on_metric_deletion(
#        service, backend, backend_usage, application_plan,
#        application):
#
#    metric_params = dict(name='for_deletion', unit='hit',
#                         friendly_name='For deletion')
#    back_metric = backend.metrics.create(params=metric_params)
#
#    limit = application_plan.limits(back_metric).create(params=dict(period='day', value=1))
#    prule = application_plan.pricing_rules(metric=back_metric).create(params={'from': 2, 'to': 99, 'cost_per_unit': 15})
#
#    back_metric.delete()
#    assert not limit.exists()
#    assert not prule.exists()
