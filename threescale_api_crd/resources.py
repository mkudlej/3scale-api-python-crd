import logging

from threescale_api_crd.defaults import DefaultClientCRD,\
    DefaultResourceCRD
import threescale_api

log = logging.getLogger(__name__)


class Services(DefaultClientCRD, threescale_api.resources.Services):
    def __init__(self, crd_client, *args, entity_name='service', entity_collection='services', **kwargs):
        threescale_api.resources.Services.__init__(self, crd_client, *args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        DefaultClientCRD.__init__(self, crd_client, *args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

# Resources
#DefaultResourceCRD,
class Service(threescale_api.resources.Service, DefaultResourceCRD):
    SPEC = {
        'apiVersion': 'capabilities.3scale.net/v1beta1',
        'kind': 'Product',
        'metadata': {
            'name': None,
            'namespace': None,
            },
        'spec': {
            'name': None,
            'providerAccountRef': {
                'name': None,
                },
            'systemName': None,
            'description': None,
            'deployment': {
                'apicastHosted': {
                    'userkey': {
                        'authUserKey': '123456',
                        'credentials': 'query',
                        },
                    },
                },
            #'backendUsages': {
            #    'backend1': {
            #        'path': '/sdfsdf',
            #        },
            #    },
            },
        }
    KEYS = {'description': 'description', 'name':'name', 'system_name':'systemName'}
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs['spec']
            entity = {}
            for k,v in spec.items():
                for c,w in Service.KEYS.items():
                    if k == w:
                        entity[c] = v
            entity['id'] = kwargs['crd'].as_dict().get('status').get('productId')

            threescale_api.resources.Service.__init__(self, entity_name=entity_name, entity=entity)
            DefaultResourceCRD.__init__(self,  entity_name=entity_name, entity=entity, **kwargs)
        else:
            threescale_api.resources.Service.__init__(self, entity_name=entity_name, **kwargs)
