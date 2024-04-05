import pytest
from tests.integration import asserts

from threescale_api_crd.resources import Limits

# With service metric
# tests important for CRD - CRU + list


@pytest.fixture()
def limit_client(application_plan, metric, limit) -> Limits:
    return application_plan.limits(metric)


def test_limit_list(limit_client):
    limits = limit_client.list()
    assert len(limits) >= 1


def test_limit_can_be_created(limit_params, limit, limit_client):
    asserts.assert_resource(limit)
    asserts.assert_resource_params(limit, limit_params)


def test_limit_can_be_read(limit_client, limit, limit_params):
    read = limit_client.read(limit.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, limit_params)


def test_limit_can_be_updated(limit_client, limit):
    lcount = limit_client.list()
    limit["value"] = 11
    lim_updated = limit.update()
    assert limit["value"] == 11 == lim_updated["value"]
    updated = limit.read()
    assert updated["value"] == 11 == limit["value"]
    assert lcount == limit_client.list()


# end of tests important for CRD - CRU + list


# With backend metric
# tests important for CRD - CRU + list


@pytest.fixture()
def backend_limit_client(application_plan, backend_metric, backend_limit) -> Limits:
    return application_plan.limits(backend_metric)


def test_backend_limit_list(backend_limit_client):
    limits = backend_limit_client.list()
    assert len(limits) >= 1


def test_backend_limit_can_be_created(
    backend_limit_params, backend_limit, backend_limit_client
):
    asserts.assert_resource(backend_limit)
    asserts.assert_resource_params(backend_limit, backend_limit_params)


def test_backend_limit_can_be_read(
    backend_limit_client, backend_limit, backend_limit_params
):
    read = backend_limit_client.read(backend_limit.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, backend_limit_params)


def test_backend_limit_can_be_updated(backend_limit_client, backend_limit):
    lcount = backend_limit_client.list()
    backend_limit["value"] = 11
    lim_updated = backend_limit.update()
    assert backend_limit["value"] == 11 == lim_updated["value"]
    updated = backend_limit.read()
    assert updated["value"] == 11 == backend_limit["value"]
    assert lcount == backend_limit_client.list()


# end of tests important for CRD - CRU + list
