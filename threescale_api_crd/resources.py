""" Module with resources for CRD for Threescale client """

import logging
import copy
import json
import base64
import requests
import openshift as ocp
import yaml
import os
import secrets

from threescale_api_crd.defaults import DefaultClientCRD,\
    DefaultResourceCRD
import threescale_api
from threescale_api_crd import constants

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
    SELECTOR = 'Product'
    NESTED = False

class Proxies(DefaultClientCRD, threescale_api.resources.Proxies):
    def __init__(self, crd_client, *args, entity_name='proxy', **kwargs):
        self.trans_item = None
        threescale_api.resources.Proxies.__init__(self, *args,
                                                   entity_name=entity_name,
                                                   **kwargs)
        DefaultClientCRD.__init__(self, *args, entity_name=entity_name, **kwargs)
        self.crd_client = crd_client
    
    def before_create(self, params, spec):
        pass

    def before_update(self, new_params, resource):
        pass
    
    def get_list(self):
        return []

    def list(self, **kwargs):
        return DefaultClientCRD.list(self, **kwargs)[0]
    
    
    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_PROXY
    KEYS = constants.KEYS_PROXY
    SELECTOR = 'Product'
    NESTED = True

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
    SELECTOR = 'Backend'
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
    SELECTOR = 'Product'
    NESTED = True

    def get_list(self):
        return self.parent.mapping_rules.list()

    def trans_item(self, key, value, obj):
        if key == 'metric_id':
            met = self.parent.metrics.read(int(obj[key]))
            return met['system_name']
        else:
            return obj[key]

    def insert_into_position(maps, params, spec):
        if 'position' in params.keys():
            maps.insert(int(params['position']) - 1, spec['spec'])
        elif 'last' in params.keys():
            maps.append(spec['spec'])
        else:
            maps.append(spec['spec'])

    def get_from_position(maps, params):
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
    SELECTOR = 'Backend'
    NESTED = True

    def get_list(self):
        return self.parent.mapping_rules.list()

    def trans_item(self, key, value, obj):
        if key == 'metric_id':
            if isinstance(obj[key], tuple):
                return obj[key][0]
            else:
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
            ide = int(params.pop('service_id'))
            sys_name = Service.id_to_system_name.get(ide, None)
            if not sys_name:
                sys_name = self.crd_client.services.read(ide)['system_name']
            spec['spec']['productSystemName'] = sys_name
        if 'body' in params.keys():
            ActiveDoc.create_secret_if_needed(params, self.crd_client.ocp_namespace)
            spec['spec']['activeDocOpenAPIRef'] = {}
            spec['spec']['activeDocOpenAPIRef']['secretRef'] = {}
            spec['spec']['activeDocOpenAPIRef']['secretRef']['name'] = params['name']

    def before_update(self, new_params, resource):
        if 'service_id' in new_params.keys():
            ide = int(new_params.pop('service_id'))
            sys_name = Service.id_to_system_name.get(ide, None)
            if not sys_name:
                sys_name = self.crd_client.services.read(ide)['system_name']
            new_params[self.KEYS['service_id']] = sys_name
        if 'body' in new_params.keys():
            ActiveDoc.create_secret_if_needed(new_params, self.crd_client.ocp_namespace)
            new_params['activeDocOpenAPIRef'] = {}
            new_params['activeDocOpenAPIRef']['secretRef'] = {}
            new_params['activeDocOpenAPIRef']['secretRef']['name'] = new_params['name']
        


    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_ACTIVE_DOC
    KEYS = constants.KEYS_ACTIVE_DOC
    SELECTOR = 'ActiveDoc'
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
            params['schema']['description'] = params['schema']['description'].strip()
            if os.linesep in params['schema']['description']:
                params['schema']['description'] = params['schema']['description'].split(os.linesep)
            else:
                params['schema']['description'] = [params['schema']['description']]

    def before_update(self, new_params, resource):
        if 'description' in new_params['schema'] and isinstance(new_params['schema']['description'], str):
            new_params['schema']['description'] = new_params['schema']['description'].strip()
            if os.linesep in new_params['schema']['description']:
                new_params['schema']['description'] = new_params['schema']['description'].split(os.linesep)
            else:
                new_params['schema']['description'] = [new_params['schema']['description']]


    CRD_IMPLEMENTED = True
    SPEC = constants.SPEC_POLICY_REG
    KEYS = constants.KEYS_POLICY_REG
    SELECTOR = 'CustomPolicyDefinition'
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
    SELECTOR = 'Product'
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
    SELECTOR = 'Backend'
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
    SELECTOR = 'Product'
    NESTED = True
    def get_list(self):
        return self.parent.backend_usages.list()

    def trans_item(self, key, value, obj):
        if key != 'backend_id':
            return obj[key]

class Policies(DefaultClientCRD, threescale_api.resources.Policies):
    """
    CRD client for Policies.
    """
    def __init__(self, crd_client, *args, entity_name='policy',
                 entity_collection='policies', **kwargs):
        self.trans_item = None
        threescale_api.resources.Policies.__init__(self, crd_client, *args,
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
    SPEC = constants.SPEC_POLICY
    KEYS = constants.KEYS_POLICY
    SELECTOR = 'Product'
    NESTED = True

    def get_list(self):
        return self.parent.proxy.list().policies.list()


    def append(self, *policies):
        pol_list = self.list()
        pol_list['policies_config'].extend(policies)
        return self.update(params=pol_list)

    def insert(self, index: int, *policies):
        pol_list = self.list()['policies_config']
        for (i, policy) in enumerate(policies):
           pol_list.insert(index + i, policy)
        return self.update(params={'policies_config': pol_list})



#class ApplicationPlans(DefaultClientCRD, threescale_api.resources.ApplicationPlans):
#    """
#    CRD client for ApplicationPlans.
#    """
#    def __init__(self, crd_client, *args, entity_name='application_plan', entity_collection='plans',
#                 **kwargs):
#        threescale_api.resources.ApplicationPlans.__init__(self, crd_client, *args,
#                                                           entity_name=entity_name,
#                                                           entity_collection=entity_collection)
#        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
#                                  entity_collection=entity_collection, **kwargs)
#        self.crd_client = crd_client
#
#    def before_create(self, params, spec):
#        pass
#
#    def before_update(self, new_params, resource):
#        pass
#
#    CRD_IMPLEMENTED = True
#    SPEC = constants.SPEC_APP_PLANS
#    KEYS = constants.KEYS_APP_PLANS
#    SELECTOR = 'Product'
#    NESTED = True
#    def get_list(self):
#        return self.parent.app_plans.list()
#
#    def trans_item(self, key, value, obj):
#        if key != 'name':
#            return obj[key]

#class Accounts(DefaultClientCRD, threescale_api.resources.Accounts):
#    """
#    CRD client for Accounts.
#    """
#    def __init__(self, crd_client, *args, entity_name='account',
#                 entity_collection='accounts', **kwargs):
#        threescale_api.resources.Accounts.__init__(self, crd_client, *args,
#                                                     entity_name=entity_name,
#                                                     entity_collection=entity_collection,
#                                                     **kwargs)
#        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
#                                  entity_collection=entity_collection, **kwargs)
#        self.crd_client = crd_client
#
#    def before_create(self, params, spec):
#        if 'username' in params:
#            pars = params.copy()
#            pars['account_name'] = pars['name']
#            pars['name'] = secrets.token_urlsafe(8)
#            self.crd_client.threescale_client.account_users.create(params=pars)
#
#
#    def before_update(self, new_params, resource):
#        pass 
#
#    CRD_IMPLEMENTED = True
#    SPEC = constants.SPEC_ACCOUNT
#    KEYS = constants.KEYS_ACCOUNT
#    SELECTOR = 'DeveloperAccount'
#    NESTED = False
#
#class AccountUsers(DefaultClientCRD, threescale_api.resources.AccountUsers):
#    """
#    CRD client for AccountUsers.
#    """
#    def __init__(self, crd_client, *args, entity_name='user',
#                 entity_collection='users', **kwargs):
#        threescale_api.resources.AccountUsers.__init__(self, crd_client, *args,
#                                                     entity_name=entity_name,
#                                                     entity_collection=entity_collection,
#                                                     **kwargs)
#        DefaultClientCRD.__init__(self, *args, entity_name=entity_name,
#                                  entity_collection=entity_collection, **kwargs)
#        self.crd_client = crd_client
#
#    def before_create(self, params, spec):
#        password = params.get('password', secrets.token_urlsafe(8))
#        password_name = AccountUser.create_password_secret(password, self.crd_client.ocp_namespace)
#        spec['spec']['passwordCredentialsRef']['name'] = password_name
#        spec['spec']['developerAccountRef']['name'] = params['account_name']
#            
#
#
#
#    def before_update(self, new_params, resource):
#        pass 
#
#    CRD_IMPLEMENTED = True
#    SPEC = constants.SPEC_ACCOUNT_USER
#    KEYS = constants.KEYS_ACCOUNT_USER
#    SELECTOR = 'DeveloperUser'
#    NESTED = False


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
            # add ids to cache
            if entity['id'] and entity['system_name']:
                Service.id_to_system_name[int(entity['id'])] = entity['system_name']
                Service.system_name_to_id[entity['system_name']] = int(entity['id'])
            auth = crd.model.spec.get('deployment', None)
            #TODO add better authentication work
            if auth:
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
    system_name_to_id = {}
    id_to_system_name = {}
    
    @property
    def proxy(self) -> 'Proxies':
        return Proxies(crd_client=self.parent, parent=self, instance_klass=Proxy)

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

#    @property
#    def app_plans(self) -> 'ApplicationPlans':
#        return ApplicationPlans(crd_client=self.parent, instance_klass=ApplicationPlan, parent=self)

class Proxy(threescale_api.resources.Proxy, DefaultResourceCRD):
    """
    CRD resource for MappingRule.
    """
    GET_PATH = 'spec/deployment'
    def __init__(self, **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            client = kwargs.get('client')
            self.spec_path = []
            # apicastHosted or ApicastSelfManaged
            if len(spec.values()): 
                self.spec_path.append(list(spec.keys())[0])
                spec = list(spec.values())[0].get('authentication', {})
                self.spec_path.append('authentication')
                # userkey or appKeyAppID or oidc
                if spec and len(spec.values()):
                    self.spec_path.append(list(spec.keys())[0])
                    spec = list(spec.values())[0].get('gatewayResponse', {})
                    self.spec_path.append('gatewayResponse')

            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_PROXY.items():
                    if key == walue:
                        entity[cey] = value

            threescale_api.resources.Proxy.__init__(self, entity=entity, **kwargs)
            DefaultResourceCRD.__init__(self, crd=crd, entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.Proxy.__init__(self, **kwargs)
            DefaultResourceCRD.__init__(self, **kwargs)
    
    
    def deploy(self) -> 'Proxy':
        LOG.info(f"[DEPLOY] CRD {self.client._entity_name} to Staging")
        url = f'{self.client.url}/deploy'
        self.client.rest.post(url)
        return self
    
    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def mapping_rules(self) -> MappingRules:
        return self.parent.mapping_rules

    @property
    def policies(self) -> 'Policies':
        return Policies(crd_client=self.parent, parent=self.parent, instance_klass=Policy)




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
                #if self.parent.__class__.__name__ == 'Backend' and ('.' not in entity['metric_id']):
                #    met_system_name = entity['metric_id'] + '.' + str(self.parent['id'])
                #else:
                met_system_name = entity['metric_id']
                met = self.parent.metrics.read_by(**{'name': met_system_name})
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
            if 'service_id' in entity:
                ide = Service.system_name_to_id.get(entity['service_id'], None)
                if not ide:
                    ide = kwargs['client'].crd_client.services.read_by_name(entity['service_id'])['id']
                entity['service_id'] = ide

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
    def __init__(self, entity_name='name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
# unit tests pass, this should be verify on real tests
#            if 'description' in spec['schema'] and isinstance(spec['schema']['description'], list):
#                spec['schema']['description'] = os.linesep.join(spec['schema']['description'])
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
            client = kwargs.get('client')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_METRIC.items():
                    if key == walue:
                        entity[cey] = value
            # simulate id because CRD has no ids
            entity['id'] = (entity['name'], entity['unit'])
            ## it is not possible to simulate id here because it is used in BackendMappingRules, which is not implemented
            #entity['id'] = Metric.system_name_to_id.get(entity['name'], None)
            #if not entity['id']:
            #    client.__class__.CRD_IMPLEMENTED = False
            #    entity['id'] = threescale_api.resources.Metrics.read_by_name(client, entity['name'] + '.' + str(client.parent.entity_id)).entity_id
            #    Metric.system_name_to_id[entity['name']] = int(entity['id'])
            #    Metric.id_to_system_name[entity['id']] = entity['name']
            #    client.__class__.CRD_IMPLEMENTED = True

            self._entity_id = entity['id']

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
    system_name_to_id = {}
    id_to_system_name = {}

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

#class ApplicationPlan(threescale_api.resources.DefaultPlanResource, DefaultResourceCRD):
#    def __init__(self, entity_name='name', **kwargs):
#        if 'spec' in kwargs:
#            spec = kwargs.pop('spec')
#            crd = kwargs.pop('crd')
#            client = kwargs.get('client')
#            entity = {}
#            for key, value in spec.items():
#                for cey, walue in constants.KEYS_APP_PLANS.items():
#                    if key == walue:
#                        entity[cey] = value
#            # simulate id because CRD has no ids
#            entity['id'] = entity['name']
#            ## it is not possible to simulate id here because it is used in Application, which is not implemented
#            #entity['id'] = ApplicationPlan.system_name_to_id.get(entity['name'], None)
#            #if not entity['id']:
#            #    client.__class__.CRD_IMPLEMENTED = False
#            #    entity['id'] = threescale_api.resources.ApplicationPlans.read_by_name(client, entity['name'])['id']
#            #    ApplicationPlan.system_name_to_id[entity['name']] = int(entity['id'])
#            #    ApplicationPlan.id_to_system_name[entity['id']] = entity['name']
#            #    client.__class__.CRD_IMPLEMENTED = True
#            self._entity_id = entity.get('id')
#
#            threescale_api.resources.ApplicationPlan.__init__(self, entity_name=entity_name,
#                                                           entity=entity, **kwargs)
#            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
#                                        entity=entity, **kwargs)
#        else:
#            # this is not here because of some backup, but because we need to have option
#            # to creater empty object without any data. This is related to "lazy load"
#            threescale_api.resources.ApplicationPlan.__init__(self, entity_name=entity_name,
#                                                           **kwargs)
#            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)
#
#    @property
#    def service(self) -> 'Service':
#        return self.parent
#
#    @property
#    def entity_id(self) -> int:
#        return self._entity_id or self._entity.get('id')
#
#    @entity_id.setter
#    def entity_id(self, value=None):
#        self._entity_id = value or self._entity.get('id')
#
#    GET_PATH = 'spec/applicationPlans'
#    system_name_to_id = {}
#    id_to_system_name = {}

#class Account(threescale_api.resources.Account, DefaultResourceCRD):
#    """
#    CRD resource for Account.
#    """
#    def __init__(self, entity_name='org_name', **kwargs):
#        if 'spec' in kwargs:
#            spec = kwargs.pop('spec')
#            crd = kwargs.pop('crd')
#            entity = {}
#            for key, value in spec.items():
#                for cey, walue in constants.KEYS_ACCOUNT.items():
#                    if key == walue:
#                        entity[cey] = value
#            entity['id'] = crd.as_dict().get('status').get('accountID')
#
#            threescale_api.resources.Account.__init__(self, entity_name=entity_name,
#                                                      entity=entity)
#            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
#                                        entity=entity, **kwargs)
#        else:
#            # this is not here because of some backup, but because we need to have option
#            # to creater empty object without any data. This is related to "lazy load"
#            threescale_api.resources.Account.__init__(self, entity_name=entity_name, **kwargs)
#            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)
#
#    #@property
#    #def users(self) -> AccountUsers:
#    #    return AccountUsers(parent=self, instance_klass=AccountUser)
#
#    GET_PATH = 'spec'
#
#class AccountUser(threescale_api.resources.AccountUser, DefaultResourceCRD):
#    """
#    CRD resource for AccountUser.
#    """
#    def __init__(self, entity_name='username', **kwargs):
#        if 'spec' in kwargs:
#            spec = kwargs.pop('spec')
#            crd = kwargs.pop('crd')
#            entity = {}
#            for key, value in spec.items():
#                for cey, walue in constants.KEYS_ACCOUNT_USER.items():
#                    if key == walue:
#                        entity[cey] = value
#            entity['id'] = crd.as_dict().get('status').get('developerUserID')
#
#            threescale_api.resources.AccountUser.__init__(self, entity_name=entity_name,
#                                                      entity=entity)
#            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
#                                        entity=entity, **kwargs)
#        else:
#            # this is not here because of some backup, but because we need to have option
#            # to creater empty object without any data. This is related to "lazy load"
#            threescale_api.resources.AccountUser.__init__(self, entity_name=entity_name, **kwargs)
#            DefaultResourceCRD.__init__(self, entity_name=entity_name, **kwargs)
#
#    @staticmethod
#    def create_password_secret(password, namespace):
#        password_ascii = str(password).encode('ascii')
#        password_enc = base64.b64encode(password_ascii)
#        spec_sec = copy.deepcopy(constants.SPEC_SECRET)
#        name = secrets.token_urlsafe(8).lower().replace('_','')
#        spec_sec['metadata']['name'] = name
#        spec_sec['metadata']['namespace'] = namespace
#        spec_sec['data']['password'] = password_enc.decode('ascii')
#        result = ocp.create(spec_sec)
#        assert result.status() == 0
#        return name
#
#    #@property
#    #def account(self) -> 'Account':
#    #    return self.parent
#
#    #@property
#    #def permissions(self) -> 'UserPermissionsClient':
#    #    return UserPermissionsClient(parent=self, instance_klass=UserPermissions)
#
#
#    GET_PATH = 'spec'


class Policy(threescale_api.resources.Policy, DefaultResourceCRD):
    """
    CRD resource for Policy.
    """
    def __init__(self, entity_name='name', **kwargs):
        if 'spec' in kwargs:
            spec = kwargs.pop('spec')
            crd = kwargs.pop('crd')
            client = kwargs.get('client')
            entity = {}
            for key, value in spec.items():
                for cey, walue in constants.KEYS_POLICY.items():
                    if key == walue:
                        entity[cey] = value
            entity['service_id'] = int(crd.as_dict().get('status', {}).get('productId', 0))
            # simulate entity_id by list of attributes
            entity['id'] = (entity['service_id'], entity['name'])
            self._entity_id = entity.get('id')

            threescale_api.resources.Policy.__init__(self, entity_name=entity_name,
                                                           entity=entity, **kwargs)
            DefaultResourceCRD.__init__(self, crd=crd, entity_name=entity_name,
                                        entity=entity, **kwargs)
        else:
            # this is not here because of some backup, but because we need to have option
            # to creater empty object without any data. This is related to "lazy load"
            threescale_api.resources.Policy.__init__(self, entity_name=entity_name,
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

    GET_PATH = 'spec/policies'
