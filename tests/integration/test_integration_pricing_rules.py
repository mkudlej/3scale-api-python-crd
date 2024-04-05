import pytest
from tests.integration import asserts

from threescale_api_crd.resources import PricingRules

# With service metric
# tests important for CRD - CRU + list


@pytest.fixture()
def prules_client(application_plan, metric, prule) -> PricingRules:
    return application_plan.pricing_rules(metric)


def test_prules_list(prules_client):
    prules = prules_client.list()
    assert len(prules) >= 1


def test_prule_can_be_created(prule_params, prule, prules_client):
    asserts.assert_resource(prule)
    asserts.assert_resource_params(prule, prule_params)


def test_prule_can_be_read(prules_client, prule, prule_params):
    read = prules_client.read(prule.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, prule_params)


def test_prule_can_be_updated(prules_client, prule):
    lcount = prules_client.list()
    prule["cost_per_unit"] = "20"
    prule_updated = prule.update()
    assert prule["cost_per_unit"] == "20" == prule_updated["cost_per_unit"]
    updated = prule.read()
    assert updated["cost_per_unit"] == "20" == prule["cost_per_unit"]
    assert lcount == prules_client.list()


# end of tests important for CRD - CRU + list


## With backend metric
## tests important for CRD - CRU + list
#
# @pytest.fixture()
# def backend_prules_client(application_plan, backend_metric, backend_limit) -> Limits:
#    return application_plan.limits(backend_metric)
#
# def test_backend_limit_list(backend_prules_client):
#    limits = backend_prules_client.list()
#    assert len(limits) >= 1
#
# def test_backend_limit_can_be_created(backend_limit_params, backend_limit, backend_prules_client):
#    asserts.assert_resource(backend_limit)
#    asserts.assert_resource_params(backend_limit, backend_limit_params)
#
#
# def test_backend_limit_can_be_read(backend_prules_client, backend_limit, backend_limit_params):
#    read = backend_prules_client.read(backend_limit.entity_id)
#    asserts.assert_resource(read)
#    asserts.assert_resource_params(read, backend_limit_params)
#
#
# def test_backend_limit_can_be_updated(backend_prules_client, backend_limit):
#    lcount = backend_prules_client.list()
#    backend_limit['value'] = 11
#    lim_updated = backend_limit.update()
#    assert backend_limit['value'] == 11 == lim_updated['value']
#    updated = backend_limit.read()
#    assert updated['value'] == 11 == backend_limit['value']
#    assert lcount == backend_prules_client.list()
#
## end of tests important for CRD - CRU + list
#
#
#
#
##@pytest.fixture()
##def limits(metric, application_plan: ApplicationPlan):
##    params = dict(period='minute', value=10)
##    application_plan.limits(metric).create(params)
##    return application_plan.limits(metric).list()
##
##
##def test_create_limit(limits):
##    assert limits is not None
##    limit = limits[0]
##    assert limit['period'] == 'minute'
##    assert limit['value'] == 10
