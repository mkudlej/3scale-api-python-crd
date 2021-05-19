import json

from tests.integration import asserts
from .asserts import assert_resource, assert_resource_params

# tests important for CRD - CRU + list

def test_activedocs_list(api, active_doc):
    active_docs = api.active_docs.list()
    assert len(active_docs) >= 1

def test_activedoc_can_be_created(api, active_docs_params, active_doc):
    assert_resource(active_doc)
    assert_resource_params(active_doc, active_docs_params)

def test_activedoc_can_be_read(api, active_docs_params, active_doc):
    read = api.active_docs.read(int(active_doc.entity_id))
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, active_docs_params)


def test_activedoc_can_be_read_by_name(api, active_docs_params, active_doc):
    account_name = active_doc['system_name']
    read = api.active_docs[account_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, active_docs_params)

def test_activedoc_can_be_updated(api, active_doc):
    des_changed = (active_doc['description'] or '') + '_changed'
    active_doc['description'] = des_changed
    gg = active_doc.update()
    assert active_doc['description'] == des_changed
    updated = active_doc.read()
    assert updated['description'] == des_changed
    assert active_doc['description'] == des_changed

# end of tests important for CRD - CRU + list

# tests to compare data in CRD and in 3scale

def test_data(api, api_origin, active_doc):
    for acd in api.active_docs.list():
        acd_origin = api_origin.active_docs.read(int(acd['id']))
        for att in acd.entity:
            # exclude CRD specific keys
            if att not in ['activeDocOpenAPIRef']:
                # body should be processed because 3scale processes json
                if att == 'body':
                    body = json.loads(acd.entity[att])
                    body_origin = json.loads(acd_origin.entity[att])
                    assert body == body_origin
                else:
                    assert acd.entity[att] == acd_origin.entity[att]
