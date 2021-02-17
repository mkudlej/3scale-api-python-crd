""" Module with default objects """

import logging
import copy
from typing import Dict, List, Optional, TYPE_CHECKING, Union, Any, Iterator

import threescale_api
import openshift as ocp

from threescale_api_crd import resources, constants

LOG = logging.getLogger(__name__)


class DefaultClientCRD(threescale_api.defaults.DefaultClient):
    def __init__(self, *args, **kwargs):
        threescale_api.defaults.DefaultClient.__init__(self, *args, **kwargs)

    def read_crd(self, selector, obj_name=None):
        sel = self.SELECTOR + '.capabilities.3scale.net'
        if obj_name:
            sel += '/' + obj_name
        LOG.info('CRD read ' + sel)
        return ocp.selector(sel).objects()

    def fetch(self, entity_id: int = None, **kwargs) -> dict:
        """Fetch the entity dictionary
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args

        Returns(dict): Resource dict from the 3scale
        """
        LOG.info(self._log_message("[FETCH] CRD Fetch ", entity_id=entity_id, args=kwargs))
        if self.__class__.CRD_IMPLEMENTED:
            list_crds = self.read_crd(self._entity_collection)
            instance_list = self._create_instance(response=list_crds)
            return ([instance for instance in instance_list
                     if instance['id'] and instance['id'] == entity_id][:1]
                    or [None])[0]

        return threescale_api.defaults.DefaultClient.fetch(self, entity_id, **kwargs)

    def _list(self, **kwargs) -> List['DefaultResource']:
        """Internal list implementation used in list or `select` methods
        Args:
            **kwargs: Optional parameters

        Returns(List['DefaultResource']):

        """
        LOG.info(self._log_message("[_LIST]", args=kwargs))
        if self.__class__.CRD_IMPLEMENTED:
            list_crds = self.read_crd(self._entity_collection)
            instance = self._create_instance(response=list_crds, collection=True)
            return instance
        return threescale_api.defaults.DefaultClient._list(self, **kwargs)

    @staticmethod
    def normalize(str_in: str):
        return str_in.replace('-', '').replace('_', '').lower()

    def create(self, params: dict = None, **kwargs) -> 'DefaultResource':
        LOG.info(self._log_message("[CREATE] Create CRD new ", body=params, args=kwargs))


        if self.__class__.CRD_IMPLEMENTED:
            spec = copy.deepcopy(self.__class__.SPEC)
            if not self.__class__.NESTED:
                params['name'] = DefaultClientCRD.normalize(params['name'])
                spec['metadata']['namespace'] = self.crd_client.ocp_namespace
                spec['metadata']['name'] = params['name']
                spec['spec']['providerAccountRef']['name'] = self.crd_client.ocp_provider_ref

            self.before_create(params, spec)

            spec['spec'] = self.translate_to_crd(params)
            for key, value in self.__class__.KEYS.items():
                if params.get(key, None) is None and \
                    value in spec['spec'] and \
                    spec['spec'][value] is None:
                    del spec['spec'][value]
            if self.__class__.NESTED:
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    if 'metric_id' not in params.keys():
                        spec['spec']['metricMethodRef'] = 'hits'
                    else:
                        met = self.parent.metrics.read(int(params['metric_id']))
                        # exception because of backend mapping rules
                        if '.' in met['system_name']:
                            spec['spec']['metricMethodRef'] = met['system_name'].split('.')[0]
                        else:
                            spec['spec']['metricMethodRef'] = met['system_name']
                mapsi = self.get_list()
                maps = {}
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    maps = []

                for mapi in mapsi:
                    if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                        maps.append(self.translate_to_crd(mapi, self.trans_item))
                    elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                        name = mapi['name']
                        maps[name] = self.translate_to_crd(mapi.entity, self.trans_item)
                    elif self.__class__.__name__ in ['BackendUsages', 'ApplicationPlans']:
                        map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                        backend_id = mapi['backend_id']
                        back = self.parent.parent.backends.read(int(backend_id))
                        maps[back['name']] = map_ret

                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    self.insert_into_position(maps, params, spec)
                    par = self.parent.update({'mapping_rules':maps})
                    maps = self.parent.mapping_rules.list()
                    return self.get_from_position(maps, params)

                elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                    name = spec['spec'].pop('name')
                    maps[name] = spec['spec']
                    par = self.parent.update({'metrics':maps})
                    maps = self.get_list()

                elif self.__class__.__name__ in ['BackendUsages']:
                    backend_id = spec['spec'].pop('backend_id')
                    back = self.parent.parent.backends.read(int(backend_id))

                    maps[back['name']] = spec['spec']
                    par = self.parent.update({'backend_usages':maps})
                    maps = self.parent.backend_usages.list()
                elif self.__class__.__name__ in ['ApplicationPlans']:
                    sys_name = spec['spec'].pop('system_name')
                    maps[sys_name] = spec['spec']
                    par = self.parent.update({'application_plans':maps})
                    maps = self.get_list()


                for mapi in maps:
                    if all([params[key] == mapi[key] for key in params.keys()]):
                        return mapi
                return None

            else:
                result = ocp.create(spec)
                assert result.status() == 0
                list_objs = self.read_crd(self._entity_collection,
                                          result.out().strip().split('/')[1])
                return (self._create_instance(response=list_objs)[:1] or [None])[0]

        return threescale_api.defaults.DefaultClient.create(self, params, **kwargs)


    def _create_instance(self, response, klass=None, collection: bool = False):
        klass = klass or self._instance_klass
        if self.__class__.CRD_IMPLEMENTED:
            extracted = self._extract_resource_crd(response, collection, klass=klass)
            instance = self._instantiate_crd(extracted=extracted, klass=klass)
        else:
            extracted = self._extract_resource(response, collection)
            instance = self._instantiate(extracted=extracted, klass=klass)
        LOG.info(f"[INSTANCE] CRD Created instance: {instance}")
        return instance

    def _extract_resource_crd(self, response, collection, klass) -> Union[List, Dict]:
        extract_params = dict(response=response, entity=self._entity_name)
        if collection:
            extract_params['collection'] = self._entity_collection
        extracted = None
        #if collection and collection in extracted:
        #    extracted = extracted.get(collection)
        if isinstance(response, list):
            if self.__class__.CRD_IMPLEMENTED and self.__class__.NESTED:
                parent_id = int(self.parent.entity_id)
                service_with_maps = {}
                for prod in response:
                    prod_dict = prod.as_dict()
                    if prod_dict is None:
                        prod_dict = {}
                    idp = int(prod_dict.get('status', {}).get('productId', 0)) or \
                            int(prod_dict.get('status', {}).get('backendId', 0))
                    if  idp == parent_id:
                        service_with_maps = prod
                        break
                spec = (DictQuery(service_with_maps.as_dict()).get(klass.GET_PATH)) or []
                if isinstance(spec, list):
                    return [{'spec': obj, 'crd': service_with_maps} for obj in spec]
                else:
                    ret = []
                    for key, obj in spec.items():
                        obj['name'] = key
                        ret.append({'spec': obj, 'crd': service_with_maps})
                    return ret
            elif self.__class__.CRD_IMPLEMENTED:
                return [{'spec': obj.as_dict()['spec'], 'crd': obj} for obj in response]
        #if entity in extracted.keys():
        #    return extracted.get(entity)
        return extracted

    def _instantiate_crd(self, extracted, klass):
        if isinstance(extracted, list):
            instance = [self.__make_instance_crd(item, klass) for item in extracted]
            return instance
        return self.__make_instance_crd(extracted, klass)

    def __make_instance_crd(self, extracted: dict, klass):
        instance = klass(client=self, spec=extracted['spec'], crd=extracted['crd']) if klass else extracted
        return instance


    def delete(self, entity_id: int = None, resource: 'DefaultResource' = None, **kwargs) -> bool:
        LOG.info(self._log_message("[DELETE] Delete CRD ", entity_id=entity_id, args=kwargs))
        if self.__class__.CRD_IMPLEMENTED and self.__class__.NESTED:
            spec = copy.deepcopy(self.SPEC)
            for key, value in self.KEYS.items():
                if resource.entity.get(key, None) is not None:
                    spec[value] = resource.entity[key]
                else:
                    del spec[value]
            mapsi = self.get_list()
            maps = {}
            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                maps = []
            for mapi in mapsi:
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    map_ret = self.translate_to_crd(mapi, self.trans_item)
                    if map_ret != spec:
                        maps.append(map_ret)
                elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        name = mapi['name']
                        maps[name] = map_ret
                elif self.__class__.__name__ in ['BackendUsages']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        backend_id = mapi['backend_id']
                        back = self.parent.parent.backends.read(int(backend_id))
                        maps[back['name']] = map_ret
                elif self.__class__.__name__ in ['ApplicationPlans']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        name = mapi['system_name']
                        maps[name] = map_ret

            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                self.parent.update({'mapping_rules':maps})
            elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                self.parent.update({'metrics':maps})
            elif self.__class__.__name__ in ['BackendUsages']:
                self.parent.update({'backend_usages':maps})
            elif self.__class__.__name__ in ['ApplicationPlans']:
                self.parent.update({'application_plans':maps})
        elif self.__class__.CRD_IMPLEMENTED:
            resource.crd.delete()
            return threescale_api.defaults.DefaultClient.delete(self, entity_id=entity_id, **kwargs)
        else:
            return threescale_api.defaults.DefaultClient.delete(self, entity_id=entity_id, **kwargs)

    def update(self, entity_id=None, params: dict = None,
               resource: 'DefaultResource' = None, **kwargs) -> 'DefaultResource':
        LOG.info(self._log_message("[UPDATE] Update CRD", body=params,
                                   entity_id=entity_id, args=kwargs))
        new_params = {**resource.entity}
        if params:
            new_params.update(params)

        if self.__class__.CRD_IMPLEMENTED and self.__class__.NESTED:
            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                new_params['id'] = (new_params['http_method'], new_params['pattern'])
            elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                new_params['id'] = (new_params['friendly_name'], new_params['unit'])
            elif self.__class__.__name__ in ['BackendUsages']:
                new_params['id'] =\
                    (new_params['path'], new_params['backend_id'], new_params['service_id'])
            elif self.__class__.__name__ in ['ApplicationPlans']:
                new_params['id'] = new_params['system_name']

            resource.entity_id = new_params['id']
            spec = self.translate_to_crd(new_params, self.trans_item)

            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules'] and \
                'metric_id' not in params.keys():
                spec['metricMethodRef'] = 'hits'

            mapsi = self.get_list()
            maps = {}
            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                maps = []
            for mapi in mapsi:
                if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                    map_ret = self.translate_to_crd(mapi, self.trans_item)
                    if map_ret != spec:
                        maps.append(map_ret)
                elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        name = mapi['name']
                        maps[name] = map_ret
                elif self.__class__.__name__ in ['BackendUsages']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        backend_id = mapi['backend_id']
                        back = self.parent.parent.backends.read(int(backend_id))
                        maps[back['name']] = map_ret
                elif self.__class__.__name__ in ['ApplicationPlans']:
                    map_ret = self.translate_to_crd(mapi.entity, self.trans_item)
                    if map_ret != spec:
                        name = mapi['system_name']
                        maps[name] = map_ret

            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                self.insert_into_position(maps, new_params, spec)
                par = self.parent.update({'mapping_rules':maps})
            elif self.__class__.__name__ in ['Metrics', 'BackendMetrics']:
                name = spec.pop('name')
                maps[name] = spec
                par = self.parent.update({'metrics':maps})
            elif self.__class__.__name__ in ['BackendUsages']:
                backend_id = spec.pop('backend_id')
                spec.pop('service_id')
                back = self.threescale_client.backends.read(int(backend_id))
                maps[back['name']] = spec
                par = self.parent.update({'backend_usages':maps})
            elif self.__class__.__name__ in ['ApplicationPlans']:
                name = spec.pop('system_name')
                maps[name] = spec
                par = self.parent.update({'application_plans':maps})

            maps = self.get_list()
            if self.__class__.__name__ in ['MappingRules', 'BackendMappingRules']:
                return self.get_from_position(maps, new_params)

            for mapi in maps:
                if all([new_params[key] == mapi[key] for key in new_params.keys()]):
                    return mapi
            return None

        elif self.__class__.CRD_IMPLEMENTED:
            self.before_update(new_params, resource)
            def _modify(apiobj):
                for key in new_params.keys():
                    if key in self.KEYS:
                        apiobj.model.spec[self.KEYS[key]] = new_params[key]

            if resource.crd is None:
                resource = resource.read()
            result, success = resource.crd.modify_and_apply(modifier_func=_modify)
            if not success:
                LOG.error(f"[INSTANCE] Update failed: {result}")
            return resource.read()


        return threescale_api.defaults.DefaultClient.update(self, entity_id=entity_id,
                                                            params=params, **kwargs)

    def translate_to_crd(self, obj, trans_item=None):
        map_ret = {}
        if not trans_item:
            trans_item = lambda key, value, obj: obj[key]
        for key, value in self.KEYS.items():
            if obj.get(key, None) is not None:
                map_ret[value] = trans_item(key, value, obj)
        return map_ret



class DefaultResourceCRD(threescale_api.defaults.DefaultResource):
    def __init__(self, crd=None, *args, **kwargs):
        threescale_api.defaults.DefaultResource.__init__(self, *args, **kwargs)
        self._crd = crd

    @property
    def crd(self):
        return self._crd or self.entity.crd

class DictQuery(dict):
    def get(self, path, default=None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break

        return val
