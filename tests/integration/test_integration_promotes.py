import pytest
from tests.integration import asserts

from threescale_api_crd.resources import Promotes

# tests important for CRD - CRU + list

# these tests should run in sequence because operator client checks if there are any changes in the product


@pytest.mark.order(1)
def test_promote_list(api, promote):
    promotes = api.promotes.list()
    assert len(promotes) >= 1


@pytest.mark.order(2)
def test_promote_can_be_created(promote_params, promote):
    asserts.assert_resource(promote)
    asserts.assert_resource_params(promote, promote_params)


@pytest.mark.order(3)
def test_promote_can_be_read(api, promote, promote_params):
    read = api.promotes.read(promote.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, promote_params)


@pytest.mark.order(4)
def test_promote_can_be_updated(api, promote):
    lcount = api.promotes.list()
    promote["deleteCR"] = False
    prom_updated = promote.update()
    assert promote["deleteCR"] == False == prom_updated["deleteCR"]
    updated = promote.read()
    assert updated["deleteCR"] == False == promote["deleteCR"]
    assert lcount == api.promotes.list()


# end of tests important for CRD - CRU + list


@pytest.mark.order(5)
def test_promote_to_production(api, mapping_rule, proxy, backend_usage):
    """
    Promotes to production. This promotion actually promotes to staging first and then to production.
    """
    mapping_rule["delta"] += 1
    mapping_rule.update()
    proxy.promote()


@pytest.mark.order(6)
def test_promote_only_to_staging(api, mapping_rule, proxy, backend_usage):
    """
    Promotes to staging only.
    """
    mapping_rule["delta"] += 1
    mapping_rule.update()
    proxy.deploy()
