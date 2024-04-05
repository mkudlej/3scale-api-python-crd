import pytest

from threescale_api.errors import ApiClientError

from tests.integration import asserts


# tests important for CRD - CRU + list
def test_should_list_methods(hits_metric, method):
    resources = hits_metric.methods.list()
    assert len(resources) > 0


def test_should_create_method(method, method_params):
    asserts.assert_resource(method)
    asserts.assert_resource_params(method, method_params)


# this is not possible in CRD, all methods are bound on 'hits'
# def test_should_not_create_method_for_custom_metric(metric, method_params):
#    resource = metric.methods.create(params=method_params, throws=False)
#    asserts.assert_errors_contains(resource, ['parent_id'])


def test_should_read_method(method, method_params):
    resource = method.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, method_params)


def test_should_update_method(hits_metric, method, updated_method_params):
    lcount = hits_metric.methods.list()
    resource = method.update(params=updated_method_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, updated_method_params)
    assert lcount == hits_metric.methods.list()


# end of tests important for CRD - CRU + list
