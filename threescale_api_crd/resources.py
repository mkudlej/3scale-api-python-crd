""" Module with resources for CRD for Threescale client """

import logging
import copy
import json
import base64
import requests
import openshift as ocp
import yaml

from threescale_api_crd.defaults import DefaultClientCRD,\
    DefaultResourceCRD
from threescale_api.defaults import DefaultPlanClient, DefaultPlanResource
import threescale_api
import threescale_api_crd.constants as constants
import threescale_api_crd.resources as resources

LOG = logging.getLogger(__name__)


class Services(DefaultClientCRD, threescale_api.resources.Services):
    """
    CRD client for Services.
    """
    def __init__(self, crd_client, *args, entity_name='service',
                 entity_collection='services', **kwargs):

        threescale_api.resources.Services.__init__(self, crd_client, *args,
                                                   entity_name=entity_name,
                                                   entity_collection=entity_collection,
                                                   **kwargs)
        DefaultClientCRD.__init__(self, crd_client, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        if 'mapping_rules' in params.keys():
            spec['mappingRules'] = params['mapping_rules']

    def before_update(self, new_params, resource):
        pass

    @property
    def metrics(self) -> 'Metrics':
        return Metrics(crd_client=self.parent, parent=self, instance_klass=Metric)

    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_SERVICE
    KEYS = constants.KEYS_SERVICE
    SELECTOR = 'products'
    NESTED = False

class Backends(DefaultClientCRD, threescale_api.resources.Backends):
    """
    CRD client for Backends.
    """
    def __init__(self, crd_client, *args, entity_name='backend_api',
                 entity_collection='backend_apis', **kwargs):

        threescale_api.resources.Backends.__init__(self, crd_client, *args,
                                                   entity_name=entity_name,
                                                   entity_collection=entity_collection,
                                                   **kwargs)
        DefaultClientCRD.__init__(self, crd_client, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        if 'mapping_rules' in params.keys():
            spec['mappingRules'] = params['mapping_rules']

    def before_update(self, new_params, resource):
        pass

    @property
    def metrics(self) -> 'BackendMetrics':
        return BackendMetrics(crd_client=self.parent, parent=self, instance_klass=BackendMetric)


    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_BACKEND
    KEYS = constants.KEYS_BACKEND
    SELECTOR = 'backends'
    NESTED = False


class MappingRules(DefaultClientCRD, threescale_api.resources.MappingRules):
    """
    CRD client for MappingRules.
    """
    def __init__(self, crd_client, *args, entity_name='mapping_rule',
                 entity_collection='mapping_rules', **kwargs):
        threescale_api.resources.MappingRules.__init__(self, *args, entity_name=entity_name,
                                                       entity_collection=entity_collection,
                                                       **kwargs)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        pass

    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_MAPPING_RULE
    KEYS = constants.KEYS_MAPPING_RULE
    SELECTOR = 'products'
    NESTED = True

    def get_list(self):
        return self.parent.mapping_rules.list()

    def trans_item(self, key, value, obj):
        if key == 'metric_id':
            met = self.parent.metrics.read(int(obj[key]))
            return met['system_name']
        else:
            return obj[key]

    def insert_into_position(self, maps, params, spec):
        if 'position' in params.keys():
            maps.insert(int(params['position']) - 1, spec['spec'])
        elif 'last' in params.keys():
            maps.append(spec['spec'])
        else:
            maps.append(spec['spec'])

    def get_from_position(self, maps, params):
        if 'position' in params.keys():
            return maps[int(params['position']) - 1]
        elif 'last' in params.keys():
            return maps[-1]
        else:
            for mapi in maps:
                if all([params[key] == mapi[key] for key in params.keys()]):
                    return mapi



class BackendMappingRules(DefaultClientCRD, threescale_api.resources.BackendMappingRules):
    """
    CRD client for Backend MappingRules.
    """
    def __init__(self, crd_client, *args, entity_name='mapping_rule',
                 entity_collection='mapping_rules', **kwargs):
        threescale_api.resources.BackendMappingRules.__init__(self, *args, entity_name=entity_name,
                                                              entity_collection=entity_collection,
                                                              **kwargs)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        pass

    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_MAPPING_RULE
    KEYS = constants.KEYS_MAPPING_RULE
    SELECTOR = 'backends'
    NESTED = True

    def get_list(self):
        return self.parent.mapping_rules.list()

    def trans_item(self, key, value, obj):
        if key == 'metric_id':
            met = self.parent.metrics.read(int(obj[key]))
            return met['system_name'].split('.')[0]
        else:
            return obj[key]

class ActiveDocs(DefaultClientCRD, threescale_api.resources.ActiveDocs):
    """
    CRD client for ActiveDocs.
    """
    def __init__(self, crd_client, *args, entity_name='api_doc',
                 entity_collection='api_docs', **kwargs):
        threescale_api.resources.ActiveDocs.__init__(self, crd_client, *args,
                                                     entity_name=entity_name,
                                                     entity_collection=entity_collection,
                                                     **kwargs)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        if 'service_id' in params.keys():
            product = self.threescale_client.services.read(int(params['service_id']))
            spec['spec']['productSystemName'] = product['system_name']
            del params['service_id']
        if 'body' in params.keys():
            ActiveDoc.create_secret_if_needed(params, self.crd_client.ocp_namespace)
            spec['spec']['activeDocOpenAPIRef'] = {}
            spec['spec']['activeDocOpenAPIRef']['secretRef'] = {}
            spec['spec']['activeDocOpenAPIRef']['secretRef']['name'] = params['name']

    def before_update(self, new_params, resource):
        if 'body' in new_params.keys():
            resources.ActiveDoc.create_secret_if_needed(new_params, self.crd_client.ocp_namespace)
            new_params['activeDocOpenAPIRef'] = {}
            new_params['activeDocOpenAPIRef']['secretRef'] = {}
            new_params['activeDocOpenAPIRef']['secretRef']['name'] = new_params['name']
        if 'service_id' in new_params.keys():
            product = self.services.read(int(new_params['service_id']))
            new_params[self.KEYS['service_id']] = product['system_name']


    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_ACTIVE_DOC
    KEYS = constants.KEYS_ACTIVE_DOC
    SELECTOR = 'activedoc'
    NESTED = False

class PoliciesRegistry(DefaultClientCRD, threescale_api.resources.PoliciesRegistry):
    """
    CRD client for PoliciesRegistry.
    """
    def __init__(self, crd_client, *args, entity_name='policy',
                 entity_collection='policies', **kwargs):
        threescale_api.resources.PoliciesRegistry.__init__(self, crd_client, *args,
                                                           entity_name=entity_name,
                                                           entity_collection=entity_collection,
                                                           **kwargs)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        if 'description' in params['schema'] and isinstance(params['schema']['description'], str):
            params['schema']['description'] = [params['schema']['description']]

    def before_update(self, new_params, resource):
        pass


    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_POLICY_REG
    KEYS = constants.KEYS_POLICY_REG
    SELECTOR = 'policy'
    NESTED = False

class Metrics(DefaultClientCRD, threescale_api.resources.Metrics):
    """
    CRD client for Metrics.
    """
    def __init__(self, crd_client, *args, entity_name='metric', entity_collection='metrics',
                 **kwargs):
        threescale_api.resources.Metrics.__init__(self, crd_client, *args,
                                                  entity_name=entity_name,
                                                  entity_collection=entity_collection)
        DefaultClientCRD.__init__(self, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        pass

    def before_update(self, new_params, resource):
        pass

    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_METRIC
    KEYS = constants.KEYS_METRIC
    SELECTOR = 'products'
    NESTED = True

    def get_list(self):
        return self.parent.metrics.list()

    def trans_item(self, key, value, obj):
        if key != 'name':
            return obj[key]

class BackendMetrics(DefaultClientCRD, threescale_api.resources.BackendMetrics):
    """
    CRD client for Backend Metrics.
    """
    def __init__(self, crd_client, *args, entity_name='metric',
                 entity_collection='metrics', **kwargs):
        threescale_api.resources.BackendMetrics.__init__(self, *args, entity_name=entity_name,
                                                         entity_collection=entity_collection)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        pass

    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_METRIC
    KEYS = constants.KEYS_METRIC
    SELECTOR = 'backends'
    NESTED = True

    def get_list(self):
        return self.parent.metrics.list()

    def trans_item(self, key, value, obj):
        if key != 'name':
            return obj[key]

class BackendUsages(DefaultClientCRD, threescale_api.resources.BackendUsages):
    """
    CRD client for BackendUsages.
    """
    def __init__(self, crd_client, *args, entity_name='backend_usage',
                 entity_collection='backend_usages', **kwargs):
        threescale_api.resources.BackendUsages.__init__(self, crd_client, *args,
                                                        entity_name=entity_name,
                                                        entity_collection=entity_collection)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        pass

    def before_update(self, new_params, resource):
        pass

    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_BACKEND_USAGE
    KEYS = constants.KEYS_BACKEND_USAGE
    SELECTOR = 'products'
    NESTED = True
    def get_list(self):
        return self.parent.backend_usages.list()

    def trans_item(self, key, value, obj):
        if key != 'backend_id':
            return obj[key]

class ApplicationPlans(DefaultClientCRD, threescale_api.resources.ApplicationPlans):
    """
    CRD client for ApplicationPlans.
    """
    def __init__(self, crd_client, *args, entity_name='application_plan', entity_collection='plans',
                 **kwargs):
        threescale_api.resources.ApplicationPlans.__init__(self, crd_client, *args,
                                                           entity_name=entity_name,
                                                           entity_collection=entity_collection)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
                                  entity_collection=entity_collection, **kwargs)
        self.crd_client = crd_client

    def before_create(self, params, spec):
        pass

    def before_update(self, new_params, resource):
        pass

    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_APP_PLANS
    KEYS = constants.KEYS_APP_PLANS
    SELECTOR = 'products'
    NESTED = True
    def get_list(self):
        return self.parent.app_plans.list()

    def trans_item(self, key, value, obj):
        if key != 'system_name':
            return obj[key]


# Resources
#DefaultResourceCRD,
class Service(threescale_api.resources.Service, DefaultResourceCRD):
    """
    CRD resource for Service.
    """
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_SERVICE.items():
                    # TODO remove this ugly list of exceptions
                    if key == walue and key != 'mappingRules':
                        entity[cey] = value
            entity['id'] = crd.as_dict().get('status').get('productId')
            auth = crd.model.spec['deployment']
            auth = auth.popitem()[1]
            if auth and 'authentication' in auth:
                auth = list(auth['authentication'].keys())[0]
                entity['backend_version'] = constants.SERVICE_AUTH[auth]

            threescale_api.resources.Service.__init__(self, entity_name=entity_name,
                                                      entity=entity)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.Service.__init__(self, entity_name=entity_name, **kwargs)
            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)

    @property
    def mapping_rules(self) -> 'MappingRules':
        return MappingRules(crd_client=self.parent, instance_klass=MappingRule, parent=self)

    GET_PATH = 'spec'

#    def get_app_plan(self):
#        return self.app_plans.list()[0]

    @property
    def policies_registry(self) -> 'PoliciesRegistry':
        return PoliciesRegistry(crd_client=self.parent, parent=self,
                                instance_klass=PoliciesRegistry)

    @property
    def metrics(self) -> 'Metrics':
        return Metrics(crd_client=self.parent, instance_klass=Metric, parent=self)

    @property
    def backend_usages(self) -> 'BackendUsages':
        return BackendUsages(crd_client=self.parent, instance_klass=BackendUsage, parent=self)

    @property
    def app_plans(self) -> 'ApplicationPlans':
        return ApplicationPlans(crd_client=self.parent, instance_klass=ApplicationPlan, parent=self)




class MappingRule(threescale_api.resources.MappingRule, DefaultResourceCRD):
    """
    CRD resource for MappingRule.
    """
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_MAPPING_RULE.items():
                    if key == walue:
                        entity[cey] = value
            # simulate entity_id by list of attributes
            entity['id'] = (entity['http_method'], entity['pattern'])
            self._entity_id = entity.get('id')

            threescale_api.resources.MappingRule.__init__(self, entity_name=entity_name,
                                                          entity=entity, **kwargs)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
            #TODO
            if 'metric_id' in entity and isinstance(entity['metric_id'], str):
                met_system_name = None
                if self.parent.__class__.__name__ == 'Backend' and ('.' not in entity['metric_id']):
                    met_system_name = entity['metric_id'] + '.' + str(self.parent['id'])
                else:
                    met_system_name = entity['metric_id']
                met = self.parent.metrics.read_by(**{'system_name': met_system_name})
                entity['metric_id'] = met['id']
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.MappingRule.__init__(self, entity_name=entity_name,
                                                          **kwargs)
            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)
    # TODO
    @property
    def proxy(self) -> 'Proxy':
        ser = self
        class FakeProxy():
            def mapping_rules(self):
                return ser.mapping_rules
        return FakeProxy()

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def entity_id(self) -> int:
        return self._entity_id or self._entity.get('id')

    @entity_id.setter
    def entity_id(self, value=None):
        self._entity_id = value or self._entity.get('id')

    GET_PATH = 'spec/mappingRules'

class ActiveDoc(threescale_api.resources.ActiveDoc, DefaultResourceCRD):
    """
    CRD resource for ActiveDoc.
    """
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_ACTIVE_DOC.items():
                    if key == walue:
                        entity[cey] = value
            entity['id'] = crd.as_dict().get('status').get('activeDocId')

            # if OAS is referenced by url:
            # 1) OAS is loaded to body
            # 2) when body is updated, secret is created and it replaces reference by url

            # if OAS is referenced by secret:
            # 1) OAS is loaded from secret and stored into body
            # 2) when body is updated, secret is changed

            if 'url' in spec['activeDocOpenAPIRef']:
                url = spec['activeDocOpenAPIRef']['url']
                entity['url'] = url
                res = requests.get(url)
                if url.endswith('.yaml') or url.endswith('.yml'):
                    entity['body'] = json.dumps(yaml.load(res.content))
                else:
                    entity['body'] = res.content
            elif 'secretRef' in spec['activeDocOpenAPIRef']:
                secret_name = spec['activeDocOpenAPIRef']['secretRef']['name']
                secret = ocp.selector('secret/' + secret_name).objects()[0]
                enc_body = list(secret.as_dict()['data'].values())[0]
                entity['body'] = base64.b64decode(enc_body).decode('ascii')

            threescale_api.resources.ActiveDoc.__init__(self, entity_name=entity_name,
                                                        entity=entity)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.ActiveDoc.__init__(self, entity_name=entity_name, **kwargs)
            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)

    GET_PATH = 'spec'

    @staticmethod
    def create_secret_if_needed(params, namespace):
        body_ascii = str(params['body']).encode('ascii')
        body_enc = base64.b64encode(body_ascii)
        spec_sec = copy.deepcopy(constants.SPEC_SECRET)
        spec_sec['metadata']['name'] = params['name']
        spec_sec['metadata']['namespace'] = namespace
        spec_sec['data'][params['name']] = body_enc.decode('ascii')
        result = ocp.selector('secret/' + params['name'])
        if result.status() == 0:
            objs = result.objects()
            if objs:
                objs[0].delete()
        result = ocp.create(spec_sec)
        assert result.status() == 0
        if 'url' in params:
            del params['url']
        del params['body']

class PolicyRegistry(threescale_api.resources.PolicyRegistry, DefaultResourceCRD):
    """
    CRD resource for PolicyRegistry.
    """
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            if 'description' in spec['schema'] and isinstance(spec['schema']['description'], list):
                spec['schema']['description'] = "".join(spec['schema']['description'])
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_POLICY_REG.items():
                    if key == walue:
                        entity[cey] = value
            entity['id'] = crd.as_dict().get('status').get('policyID')

            threescale_api.resources.PolicyRegistry.__init__(self, entity_name=entity_name,
                                                             entity=entity)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.PolicyRegistry.__init__(self, entity_name=entity_name,
                                                             **kwargs)
            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)

    GET_PATH = 'spec'

class Backend(threescale_api.resources.Backend, DefaultResourceCRD):
    """
    CRD resource for Backend.
    """
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_BACKEND.items():
                    # TODO remove this ugly list of exceptions
                    if key == walue and key != 'mappingRules':
                        entity[cey] = value
            entity['id'] = crd.as_dict().get('status').get('backendId')

            threescale_api.resources.Backend.__init__(self, entity_name=entity_name,
                                                      entity=entity)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.Backend.__init__(self, entity_name=entity_name, **kwargs)
            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)

    @property
    def mapping_rules(self) -> 'BackendMappingRules':
        return BackendMappingRules(crd_client=self.parent, parent=self,
                                   instance_klass=BackendMappingRule)
    @property
    def metrics(self) -> 'BackendMetrics':
        return BackendMetrics(crd_client=self.parent, parent=self,
                              instance_klass=BackendMetric)

    GET_PATH = 'spec'

class BackendMappingRule(MappingRule):
    """
    CRD resource for Backend MappingRule.
    """
    def __init__(self, **kwargs):
        MappingRule.__init__(self, **kwargs)

    GET_PATH = 'spec/mappingRules'

class Metric(threescale_api.resources.Metric, DefaultResourceCRD):
    """
    CRD resource for Metric.
    """
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_METRIC.items():
                    if key == walue:
                        entity[cey] = value
            # simulate entity_id by list of attributes
            entity['id'] = (entity['friendly_name'], entity['unit'])
            self._entity_id = entity.get('id')

            threescale_api.resources.Metric.__init__(self, entity_name=entity_name,
                                                     entity=entity, **kwargs)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.Metric.__init__(self, entity_name=entity_name,
                                                     **kwargs)
            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def entity_id(self) -> int:
        return self._entity_id or self._entity.get('id')

    @entity_id.setter
    def entity_id(self, value=None):
        self._entity_id = value or self._entity.get('id')


    GET_PATH = 'spec/metrics'

class BackendMetric(Metric):
    """
    CRD resource for Backend Metric.
    """
    def __init__(self, **kwargs):
        Metric.__init__(self, **kwargs)

    GET_PATH = 'spec/metrics'

class BackendUsage(threescale_api.resources.BackendUsage, DefaultResourceCRD):
    """
    CRD resource for BackendUsage.
    """
    def __init__(self, entity_name='system_name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            client = kwargs.get('client')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_BACKEND_USAGE.items():
                    if key == walue:
                        entity[cey] = value
            entity['service_id'] = int(crd.as_dict().get('status', {}).get('productId', 0))
            back = client.threescale_client.backends.read_by_name(spec['name'])
            entity['backend_id'] = int(back['id'])
            # simulate entity_id by list of attributes
            entity['id'] = (entity['path'], entity['backend_id'], entity['service_id'])
            self._entity_id = entity.get('id')

            threescale_api.resources.BackendUsage.__init__(self, entity_name=entity_name,
                                                           entity=entity, **kwargs)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.BackendUsage.__init__(self, entity_name=entity_name,
                                                           **kwargs)
            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def entity_id(self) -> int:
        return self._entity_id or self._entity.get('id')

    @entity_id.setter
    def entity_id(self, value=None):
        self._entity_id = value or self._entity.get('id')

    GET_PATH = 'spec/backendUsages'

class ApplicationPlan(DefaultPlanResource):
    def __init__(self, entity_name='system_name', **kwargs):
        DefaultPlanResource.__init__(self, entity_name=entity_name, **kwargs)

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def entity_id(self) -> int:
        return self._entity_id or self._entity.get('id')

    @entity_id.setter
    def entity_id(self, value=None):
        self._entity_id = value or self._entity.get('id')

    GET_PATH = 'spec/applicationPlans'
