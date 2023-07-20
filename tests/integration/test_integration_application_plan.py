import pytest
import secrets

from tests.integration import asserts

# tests important for CRD - CRU + list
def test_application_plans_list(service):
    app_plans = service.app_plans.list()
    assert len(app_plans) == 1

def test_application_plan_can_be_created(service, application_plan_params, application_plan):
    asserts.assert_resource(application_plan)
    asserts.assert_resource_params(application_plan, application_plan_params)

# IDs cannot be used in nested objects
#def test_application_plan_can_be_read(service, application_plan_params, application_plan):
#    read = service.app_plans.read(int(application_plan.entity_id))
#    asserts.assert_resource(read)
#    asserts.assert_resource_params(read, application_plan)


def test_application_plan_can_be_read_by_name(service, application_plan_params, application_plan):
    name = application_plan['system_name']
    read = service.app_plans[name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, application_plan)

@pytest.fixture(scope='module')
def update_params():
    suffix = secrets.token_urlsafe(8)
    return dict(cost_per_month='12.00', setup_fee='50.00', state_event='publish')

def test_application_plan_can_be_updated(service, application_plan, update_params):
    lcount = len(service.app_plans.list())
    updated_app_plan = application_plan.update(update_params)
    asserts.assert_resource(updated_app_plan)
    asserts.assert_resource_params(updated_app_plan, update_params)
    assert len(service.app_plans.list()) == lcount

# end of tests important for CRD - CRU + list
