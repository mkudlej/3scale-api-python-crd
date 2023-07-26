""" Module with default objects """

import logging
import copy
import random
import string
import time
from typing import Dict, List, Union

import threescale_api
import openshift as ocp

from threescale_api_crd import resources, constants, client

LOG = logging.getLogger(__name__)


class DefaultClientCRD(threescale_api.defaults.DefaultClient):
    """Default CRD client."""

    CRD_IMPLEMENTED = False
    SPEC = None
    NESTED = False
    SELECTOR = None
    KEYS = None
    ID_NAME = None

    def __init__(self, parent=None, instance_klass=None, entity_name=None, entity_collection=None):
        super().__init__(parent=parent, instance_klass=instance_klass,
                         entity_name=entity_name, entity_collection=entity_collection)

    def get_list(self, typ='normal'):
        """ Returns list of entities. """
        return []

    def trans_item(self, key, value, obj):
        """ Translate entity to CRD. """
        return []

    def read_crd(self, selector, obj_name=None):
        """Read current CRD definition based on selector and/or object name."""
        sel = self.SELECTOR + '.capabilities.3scale.net'
        if obj_name:
            sel += '/' + obj_name
        LOG.info('CRD read %s', str(sel))
        return ocp.selector(sel).objects()

    def is_crd_implemented(self):
        """Returns True is crd is implemented in the client"""
        return self.__class__.CRD_IMPLEMENTED

    def enable_crd_implemented(self):
        """Set True to crd is implemented attribute"""
        self.__class__.CRD_IMPLEMENTED = True

    def disable_crd_implemented(self):
        """Set False to crd is implemented attribute"""
        self.__class__.CRD_IMPLEMENTED = False

    def fetch(self, entity_id: int = None, **kwargs):
        """Fetch the entity dictionary
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args

        Returns(dict): Resource dict from the 3scale
        """
        LOG.info(self._log_message("[FETCH] CRD Fetch ", entity_id=entity_id, args=kwargs))

        if self.is_crd_implemented():
            list_crds = self.read_crd(self._entity_collection)
            instance_list = self._create_instance(response=list_crds)
            ret = []
            if isinstance(instance_list, list):
                ret = ([instance for instance in instance_list
                    if (instance.entity_id and instance.entity_id == entity_id) or
                    entity_id is None][:1] or [None])[0]
            else:
                # proxy.fetch exception
                ret = instance_list
            return ret
        return threescale_api.defaults.DefaultClient.fetch(self, entity_id, **kwargs)

    def exists(self, entity_id=None, **kwargs) -> bool:
        """Check whether the resource exists
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args

        Returns(bool): True if the resource exists
        """
        LOG.info(self._log_message("[EXIST] CRD Resource exist ", entity_id=entity_id, args=kwargs))
        return self.fetch(entity_id, **kwargs)


    def _list(self, **kwargs) -> List['DefaultResource']:
        """Internal list implementation used in list or `select` methods
        Args:
            **kwargs: Optional parameters

        Returns(List['DefaultResource']):

        """
        LOG.info(self._log_message("[_LIST] CRD", args=kwargs))
        if self.is_crd_implemented():
            list_crds = self.read_crd(self._entity_collection)
            instance = self._create_instance(response=list_crds, collection=True)
            return instance
        return threescale_api.defaults.DefaultClient._list(self, **kwargs)

    @staticmethod
    def normalize(str_in: str):
        """Some values in CRD cannot contain some characters."""
        return str_in.replace('-', '').replace('_', '').lower()

    def create(self, params: dict = None, **kwargs) -> 'DefaultResource':
        LOG.info(self._log_message("[CREATE] Create CRD new ", body=params, args=kwargs))
        if self.is_crd_implemented():
            spec = copy.deepcopy(self.SPEC)
            name = params.get('name') or params.get('username') # Developer User exception
            if name is not None:
                name = self.normalize(name)
                if params.get('name'):
                    params['name'] = name
                else:
                    params['username'] = name
            else:
                name = self.normalize(''.join(random.choice(string.ascii_letters) for _ in range(16)))

            if not self.NESTED:
                spec['metadata']['namespace'] = self.threescale_client.ocp_namespace
                spec['metadata']['name'] = name
                if self.__class__.__name__ not in ['Tenants']:
                    if self.threescale_client.ocp_provider_ref is None:
                        spec['spec'].pop('providerAccountRef')
                    else:
                        spec['spec']['providerAccountRef']['name'] = self.threescale_client.ocp_provider_ref
                        spec['spec']['providerAccountRef']['namespace'] = self.threescale_client.ocp_namespace
            self.before_create(params, spec)

            spec['spec'].update(self.translate_to_crd(params))
            for key, value in self.KEYS.items():
                if params.get(key, None) is None and \
                    value in spec['spec'] and \
                    spec['spec'][value] is None:
                    del spec['spec'][value]
            if self.NESTED:
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    if 'metric_id' not in params.keys():
                        spec['spec']['metricMethodRef'] = 'hits'
                    elif isinstance(params['metric_id'], int):
                        met = self.parent.metrics.read(int(params['metric_id']))
                        # exception because of backend mapping rules
                        name = met.entity.get('system_name', met.entity.get('name'))
                        if '.' in met['system_name']:
                            spec['spec']['metricMethodRef'] = name.split('.')[0]
                        spec['spec']['metricMethodRef'] = name
                    else:
                        # metric id is tuple
                        spec['spec']['metricMethodRef'] = params['metric_id'][0]
                mapsi = self.get_list(typ='full')
                maps = {}
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules', 'Limits', 'PricingRules']:
                    maps = []

                for mapi in mapsi:
                    if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                        maps.append(self.translate_to_crd(mapi.entity, self.trans_item))
                    elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                        name = mapi[self.ID_NAME]
                        maps[name] = self.translate_to_crd(mapi.entity, self.trans_item)
                    elif self.__class__.__name__ in ['BackendUsages']:
                        map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                        backend_id = mapi['backend_id']
                        back = self.parent.parent.backends.read(int(backend_id))
                        maps[back[self.ID_NAME]] = map_ret
                    elif self.__class__.__name__ in ['ApplicationPlans']:
                        name = mapi[self.ID_NAME]
                        maps[name] = self.translate_to_crd(mapi.entity, self.trans_item)
                    elif self.__class__.__name__ in ['Limits']:
                        if params['period'] != mapi['period'] or \
                            params['metric_name'] != mapi['metric_name'] or \
                            params['plan_id'] != mapi['plan_id']:
                            ins = self.translate_to_crd(mapi.entity)
                            ins['metricMethodRef'] = {'systemName': mapi['metric_name']}
                            if 'backend_name' in mapi.entity:
                                ins['metricMethodRef']['backend'] = mapi['backend_name']
                            maps.append(ins)
                    elif self.__class__.__name__ in ['PricingRules']:
                        if params['min'] != mapi['min'] or params['max'] != mapi['max'] or \
                            params['metric_name'] != mapi['metric_name'] or \
                            params['plan_id'] != mapi['plan_id']:
                            ins = self.translate_to_crd(mapi.entity)
                            ins['metricMethodRef'] = {'systemName': mapi['metric_name']}
                            if 'backend_name' in mapi.entity:
                                ins['metricMethodRef']['backend'] = mapi['backend_name']
                            maps.append(ins)


                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    resources.MappingRules.insert_into_position(maps, params, spec)
                    self.parent.update({'mapping_rules':maps})
                    maps = self.parent.mapping_rules.list()
                    return resources.MappingRules.get_from_position(maps, params)

                elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                    name = params.get('name', params.get('system_name', 'hits'))
                    if 'name' in spec['spec']:
                        spec['spec'].pop('name')
                    maps[name] = spec['spec']
                    par = self.parent.update({'metrics':maps})
                    maps = self.get_list()
                elif self.__class__.__name__ in ['BackendUsages']:
                    backend_id = spec['spec'].pop('backend_id')
                    back = self.parent.parent.backends.read(int(backend_id))

                    maps[back[self.ID_NAME]] = spec['spec']
                    par = self.parent.update({'backend_usages':maps})
                    maps = self.parent.backend_usages.list()
                elif self.__class__.__name__ in ['ApplicationPlans']:
                    if self.ID_NAME in spec['spec']:
                        params[self.ID_NAME] = DefaultClientCRD.normalize(spec['spec'].pop(self.ID_NAME))
                    else:
                        params[self.ID_NAME] = DefaultClientCRD.normalize(spec['spec'].pop('name'))
                    maps[params[self.ID_NAME]] = spec['spec']
                    par = self.parent.update({'application_plans':maps})
                    maps = self.get_list()
                elif self.__class__.__name__ in ['Limits']:
                    maps = resources.Limits.insert_to_list(maps, params, spec)
                    self.parent.update({'limits':maps})
                    maps = self.get_list(typ='normal')
                    return resources.Limits.get_from_list(maps, params, spec)
                elif self.__class__.__name__ in ['PricingRules']:
                    maps = resources.PricingRules.insert_to_list(maps, params, spec)
                    self.parent.update({'pricingRules':maps})
                    maps = self.get_list(typ='normal')
                    return resources.PricingRules.get_from_list(maps, params, spec)
                for mapi in maps:
                    if all([params[key] == mapi[key] for key in params.keys()]):
                        return mapi
                return None

            else:
                result = ocp.create(spec)
                assert result.status() == 0
                list_objs = self.read_crd(self._entity_collection,
                                          result.out().strip().split('/')[1])
                created_objects = []
                counter = 10
                while len(list_objs) > 0 and counter > 0:
                    list_objs2 = []
                    for obj in list_objs:
                        obj.refresh()
                        status = obj.as_dict().get('status', None)
                        if status:
                            new_id = status.get(self.ID_NAME, 0)
                            # exception because of https://issues.redhat.com/browse/THREESCALE-8273
                            if self.__class__.__name__ in ['Tenants']:
                                if status.get('adminId', None) and status.get('tenantId', None):
                                    created_objects.append(obj)
                            elif self.__class__.__name__ in ['Promotes', 'Applications']:
                                state = {'Ready': status['conditions'][0]['status'] == 'True'}
                                if state['Ready']:
                                    created_objects.append(obj)
                                else:
                                    list_objs2.append(obj)
                            else:
                                state = {'Failed': True, 'Invalid': True, 'Synced': False, 'Ready': False}
                                for sta in status['conditions']:
                                    state[sta['type']] = (sta['status'] == 'True')
                                if state['Failed'] or state['Invalid'] or\
                                    (not (state['Synced'] or state['Ready'])) or\
                                    (new_id == 0):
                                    list_objs2.append(obj)
                                else:
                                    created_objects.append(obj)
                        else:
                            list_objs2.append(obj)
                    list_objs = list_objs2
                    if not list_objs:
                        time.sleep(20)
                    counter -= 1

                instance = (self._create_instance(response=created_objects)[:1] or [None])[0]
                return instance

        return threescale_api.defaults.DefaultClient.create(self, params, **kwargs)


    def _create_instance(self, response, klass=None, collection: bool = False):
        klass = klass or self._instance_klass
        if self.is_crd_implemented():
            extracted = self._extract_resource_crd(response, collection, klass=klass)
            instance = self._instantiate_crd(extracted=extracted, klass=klass)
        else:
            extracted = self._extract_resource(response, collection)
            instance = self._instantiate(extracted=extracted, klass=klass)
        LOG.info("[INSTANCE] CRD Created instance: %s", str(instance))
        return instance

    def _extract_resource_crd(self, response, collection, klass) -> Union[List, Dict]:
        extract_params = dict(response=response, entity=self._entity_name)
        if collection:
            extract_params['collection'] = self._entity_collection
        extracted = None
        #if collection and collection in extracted:
        #    extracted = extracted.get(collection)
        if isinstance(response, list):
            if self.is_crd_implemented() and self.NESTED:
                parent_id = int(self.topmost_parent().entity_id)
                service_with_maps = {}
                for prod in response:
                    prod_dict = prod.as_dict()
                    if prod_dict is None:
                        prod_dict = {}
                    idp = int(prod_dict.get('status', {}).get(self.topmost_parent().client.ID_NAME, 0))
                    if  idp == parent_id:
                        service_with_maps = prod
                        break
                spec = {}
                if service_with_maps != {}:
                    spec = (DictQuery(service_with_maps.as_dict()).get(klass.GET_PATH or self.get_path())) or []
                if isinstance(spec, list):
                    return [{'spec': obj, 'crd': service_with_maps} for obj in spec]
                elif 'apicastHosted' not in spec.keys(): # exception for Proxy
                    ret = []
                    for key, obj in spec.items():
                        obj[self.ID_NAME] = key

                        ret.append({'spec': obj, 'crd': service_with_maps})
                    return ret
                else:
                    return [{'spec': spec, 'crd': service_with_maps}]
            elif self.is_crd_implemented():
                return [{'spec': obj.as_dict()['spec'], 'crd': obj} for obj in response]
        #if entity in extracted.keys():
        #    return extracted.get(entity)
        return extracted

    def _instantiate_crd(self, extracted, klass):
        if isinstance(extracted, list):
            instance = [self.__make_instance_crd(item, klass) for item in extracted]
            if self.__class__.__name__ == 'Policies':
                return {'policies_config': instance}
            if self.__class__.__name__ == 'Proxies':
                return instance[0]
            if self.__class__.__name__ in ['Limits', 'PricingRules']:
                # it is needed to distinguish between getting metric's limits(normal) or all limits(full)
                if (resources.Limits.LIST_TYPE == 'normal' and self.__class__.__name__ == 'Limits') or (resources.PricingRules.LIST_TYPE == 'normal' and self.__class__.__name__ == 'PricingRules'):
                    if self.metric.__class__.__name__ == 'BackendMetric':
                        return [obj for obj in instance \
                                if self.metric['name'] == obj['metric_name'] and \
                                self.metric.parent['system_name'] == obj['backend_name']]
                    else:
                        return [obj for obj in instance \
                                if self.metric['name'] == obj['metric_name'] and \
                                'backend_name' not in obj.entity]
                else:
                    return [obj for obj in instance]
            return instance
        return self.__make_instance_crd(extracted, klass)

    def __make_instance_crd(self, extracted: dict, klass):
        instance = klass(client=self, spec=extracted['spec'], crd=extracted['crd']) if klass else extracted
        return instance


    def delete(self, entity_id: int = None, resource: 'DefaultResource' = None, **kwargs) -> bool:
        """ Method deletes resource. """
        LOG.info(self._log_message("[DELETE] Delete CRD ", entity_id=entity_id, args=kwargs))
        if self.is_crd_implemented() and self.NESTED:
            spec = self.translate_to_crd(resource.entity, self.trans_item)
            mapsi = self.get_list()
            maps = {}
            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules', 'Limits', 'PricingRules']:
                maps = []
            for mapi in mapsi:
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        maps.append(map_ret)
                elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        name = mapi[self.ID_NAME]
                        maps[name] = map_ret
                elif self.__class__.__name__ in ['BackendUsages']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        backend_id = mapi['backend_id']
                        back = self.parent.parent.backends.read(int(backend_id))
                        maps[back[self.ID_NAME]] = map_ret
                elif self.__class__.__name__ in ['ApplicationPlans']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        name = mapi[self.ID_NAME]
                        maps[name] = map_ret
                elif self.__class__.__name__ in ['Limits', 'PricingRules']:
                    spec = self.translate_to_crd(resource.entity)
                    map_ret = self.translate_to_crd(mapi.entity)
                    if map_ret != spec:
                        maps.append(map_ret)

            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                self.parent.update({'mapping_rules':maps})
            elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                self.parent.update({'metrics':maps})
            elif self.__class__.__name__ in ['BackendUsages']:
                self.parent.update({'backend_usages':maps})
            elif self.__class__.__name__ in ['ApplicationPlans']:
                self.parent.update({'application_plans':maps})
            elif self.__class__.__name__ in ['Limits']:
                par = self.parent.update({'limits': maps})
            elif self.__class__.__name__ in ['PricingRules']:
                par = self.parent.update({'pricingRules': maps})
            return True
        elif self.is_crd_implemented():
            resource.crd.delete()
            if self.__class__.__name__ not in ['Services', 'Backends', 'Tenants', 'Accounts', 'AccountUsers', 'Promotes', 'OpenApis', 'Applications']:
                return threescale_api.defaults.DefaultClient.delete(self, entity_id=entity_id, **kwargs)
            else:
                return True
        else:
            return threescale_api.defaults.DefaultClient.delete(self, entity_id=entity_id, **kwargs)

    def update(self, entity_id=None, params: dict = None,
               resource: 'DefaultResource' = None,
               **kwargs) -> 'DefaultResource':
        LOG.info(self._log_message("[UPDATE] Update CRD", body=params,
                                   entity_id=entity_id, args=kwargs))
        new_params = {}
        if resource:
            new_params = {**resource.entity}
        if params:
            new_params.update(params)
#TODO change ids for objects which require ids
        if self.is_crd_implemented() and self.NESTED:
            spec = {}

            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                new_params['id'] = (new_params['http_method'], new_params['pattern'])
            elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                new_params['id'] = (new_params['name'], new_params['unit'])
            elif self.__class__.__name__ in ['BackendUsages']:
                new_params['id'] =\
                    (new_params['path'], new_params['backend_id'], new_params['service_id'])
            elif self.__class__.__name__ in ['ApplicationPlans']:
                self.before_update(new_params, resource)
                new_params['id'] = new_params['system_name']
            elif self.__class__.__name__ in ['Proxies']:
                new_params['id'] = self.parent.entity_id
            elif self.__class__.__name__ in ['Policies']:
                new_params = new_params['policies_config']
                # this should be done because list of policies is already
                # constructed list and not just one item
                spec = []
                for item in new_params:
                    if hasattr(item, 'entity'):
                        item = item.entity
                    spec.append(self.translate_to_crd(item, self.trans_item))
            elif self.__class__.__name__ in ['Limits', 'PricingRules']:
                new_params['id'] = self.get('id')
            if resource and 'id' in params:
                resource.entity_id = params['id']
            # see above comment
            if self.__class__.__name__ not in ['Policies']:
                spec = self.translate_to_crd(new_params, self.trans_item)

            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules'] and \
                'metric_id' not in params.keys():
                spec['metricMethodRef'] = 'hits'

            mapsi = self.get_list()
            maps = {}
            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules', 'Limits', 'PricingRules']:
                maps = []

            # TODO this for should be replaced by insert_to_list method
            for mapi in mapsi:
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if not (map_ret['httpMethod'] == spec['httpMethod'] and map_ret['pattern'] == spec['pattern']):
                        maps.append(map_ret)
                elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        name = mapi[self.ID_NAME]
                        maps[name] = map_ret
                elif self.__class__.__name__ in ['BackendUsages']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        backend_id = mapi['backend_id']
                        back = self.parent.parent.backends.read(int(backend_id))
                        maps[back[self.ID_NAME]] = map_ret
                elif self.__class__.__name__ in ['ApplicationPlans']:
                    if mapi['id'] != new_params['id']:
                        map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                        maps[mapi[self.ID_NAME]] = map_ret
                elif self.__class__.__name__ in ['Limits', 'PricingRules']:
                    map_ret = self.translate_to_crd(mapi.entity)
                    maps.append(map_ret)

            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                resources.MappingRules.insert_into_position(maps, new_params, spec)
                par = self.parent.update({'mapping_rules':maps})
            elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                name = new_params.get(self.ID_NAME)
                maps[name] = spec
                par = self.parent.update({'metrics':maps})
            elif self.__class__.__name__ in ['BackendUsages']:
                backend_id = spec.pop('backend_id')
                spec.pop('service_id')
                back = self.threescale_client.backends.read(int(backend_id))
                maps[back[self.ID_NAME]] = spec
                par = self.parent.update({'backend_usages':maps})
            elif self.__class__.__name__ in ['ApplicationPlans']:
                maps[new_params['id']] = spec
                par = self.parent.update({'application_plans':maps})
            elif self.__class__.__name__ in ['Proxies']:
                obj = {}
                iter_obj = obj
                # service.proxy.oidc.update(params={"oidc_configuration": DEFAULT_FLOWS})

                for path in resource.spec_path:
                    if path not in iter_obj:
                        if path == resource.spec_path[-1]:
                            iter_obj[path] = spec
                            if resource.oidc['oidc_configuration']:
                                auth_flow = self.translate_specific_to_crd(
                                        resource.oidc['oidc_configuration'],
                                        constants.KEYS_OIDC)
                                iter_obj[path]['authenticationFlow'] = auth_flow
                            if resource.responses or\
                                (set(new_params.keys()).intersection(set(constants.KEYS_PROXY_RESPONSES))):
                                resource.responses = True
                                resps = self.translate_specific_to_crd(new_params, constants.KEYS_PROXY_RESPONSES)
                                iter_obj[path]['gatewayResponse'] = resps
                            if resource.security:
                                sec = self.translate_specific_to_crd(new_params, constants.KEYS_PROXY_SECURITY)
                                iter_obj[path]['gatewayResponse'] = sec

                        else:
                            iter_obj[path] = {}
                    iter_obj = iter_obj[path]

                par = self.parent.update({'deployment': obj})
            elif self.__class__.__name__ in ['Policies']:
                par = self.parent.update({'policies': spec})
            elif self.__class__.__name__ in ['Limits']:
                spec = self.translate_to_crd(params)
                maps = resources.Limits.insert_to_list(maps, params, {'spec': spec})
                par = self.parent.update({'limits': maps})
            elif self.__class__.__name__ in ['PricingRules']:
                spec = self.translate_to_crd(params)
                maps = resources.PricingRules.insert_to_list(maps, params, {'spec': spec})
                par = self.parent.update({'pricingRules': maps})

            maps = self.get_list()
            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                return resources.MappingRules.get_from_position(maps, new_params)

            if self.__class__.__name__ in ['Proxies']:
                return par.proxy.list()

            if self.__class__.__name__ in ['Policies']:
                return maps

            checked_keys = [key for key in new_params.keys() if key not in ['id']]
            for mapi in maps:
                if all([new_params[key] == mapi[key] for key in checked_keys]):
                    return mapi
            return None

        elif self.is_crd_implemented():
            new_params = copy.deepcopy(new_params)
            self.before_update(new_params, resource)
            new_spec = self.translate_to_crd(new_params, self.trans_item)
            if self.__class__.__name__ in ['Applications']:
                new_spec['productCR'] = {}
                new_spec['productCR']['name'] = new_params['service_name']
                new_spec['accountCR'] = {}
                new_spec['accountCR']['name'] = new_params['account_name']
            if resource.crd is None:
                resource = resource.read()
                if isinstance(resource, list):
                    resource = resource[0]
            resource.crd.refresh()
            new_crd = resource.crd.as_dict()
            new_crd['spec'].update(new_spec)
            if self.__class__.__name__ not in ['Tenants']:
                if self.threescale_client.ocp_provider_ref is None:
                    new_crd['spec'].pop('providerAccountRef', None)
                else:
                    new_crd['spec']['providerAccountRef'] = {
                        'name': self.threescale_client.ocp_provider_ref,
                        'namespace': self.threescale_client.ocp_namespace
                    }
            resource.crd.model = ocp.Model(new_crd)
            result = resource.crd.replace()

            if result.status():
                LOG.error("[INSTANCE] Update CRD failed: %s", str(result))
                raise Exception(str(result))
            return self.read(resource.entity_id)


        return threescale_api.defaults.DefaultClient.update(self, entity_id=entity_id,
                                                            params=params, **kwargs)

    def translate_to_crd(self, obj, trans_item=None):
        """Translate object attributes into object ready for merging into CRD."""
        map_ret = {}
        if not trans_item:
            trans_item = lambda key, value, obj: obj[key]
        for key, value in self.KEYS.items():
            LOG.debug("%s, %s, %s, %s", str(key), str(value), str(obj), str(type(obj)))
            if obj.get(key, None) is not None:
                set_value = trans_item(key, value, obj)
                if set_value is not None:
                    map_ret[value] = set_value


        return map_ret



class DefaultResourceCRD(threescale_api.defaults.DefaultResource):
    """Default CRD resource."""
    GET_PATH = None
    def __init__(self, *args, crd=None, **kwargs):
        super().__init__(**kwargs)
        self._crd = crd

    @property
    def crd(self):
        """CRD object property."""
        return self._crd or self.entity.get('crd', None)

    @crd.setter
    def crd(self, value):
        self._crd = value

    @property
    def entity_id(self) -> int:
        return self._entity_id or self._entity.get('id') or self.get_id_from_crd()

    @entity_id.setter
    def entity_id(self, value):
        self._entity_id = value

    def get_id_from_crd(self):
        """Returns object id extracted from CRD."""
        if self.client.NESTED:
            return None
        counter = 5
        while counter > 0:
            self.crd = self.crd.refresh()
            status = self.crd.as_dict()['status']
            ret_id = status.get(self.client.ID_NAME, None)
            if ret_id:
                return ret_id
            time.sleep(20)
            counter -= 1

        return None

    def get_path(self):
        """
        This function is usefull only for Limits and PricingRules and\
        it should be redefined there.
        """
        return self.__class__.GET_PATH


class DictQuery(dict):
    """Get value from nested dictionary."""
    def get(self, path, default=None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in list(val)]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break

        return val
