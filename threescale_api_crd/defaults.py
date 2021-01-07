import logging
from typing import Dict, List, Optional, TYPE_CHECKING, Union, Any, Iterator

import threescale_api
import openshift as ocp

import copy
from threescale_api_crd import resources

LOG = logging.getLogger(__name__)


class DefaultClientCRD(threescale_api.defaults.DefaultClient):
    def __init__(self, *args, **kwargs):
        threescale_api.defaults.DefaultClient.__init__(self, *args, **kwargs)
        self._ocp = ocp
        self._get_path = ['spec']
        self._list_crds = []

    @property
    def ocp(self):
        return self._ocp

    def read_crd(self, selector, obj_name=None):
        if selector == 'services':
            selector = 'products'
        sel = selector + '.capabilities.3scale.net'
        if obj_name:
            sel += '/' + obj_name
        return ocp.selector(sel).objects()
    
    @property
    def get_path(self):
        return self._get_path

    def fetch(self, entity_id: int = None, **kwargs) -> dict:
        """Fetch the entity dictionary
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args

        Returns(dict): Resource dict from the 3scale
        """
        LOG.debug(self._log_message("[FETCH] CRD Fetch ", entity_id=entity_id, args=kwargs))
        if self.__class__.__name__ == 'Services':
            self._list_crds = self.read_crd(self._entity_collection)
            instance_list = self._create_instance(response=self._list_crds)
            return ([instance for instance in instance_list if int(instance['id']) == int(entity_id)][:1] or [None])[0]
        return threescale_api.defaults.DefaultClient.fetch(self, entity_id, **kwargs)

    def _list(self, **kwargs) -> List['DefaultResource']:
        """Internal list implementation used in list or `select` methods
        Args:
            **kwargs: Optional parameters

        Returns(List['DefaultResource']):

        """
        if self.__class__.__name__ == 'Services':
            self._list_crds = self.read_crd(self._entity_collection)
            instance = self._create_instance(response=self._list_crds, collection=True)
            return instance
        return threescale_api.defaults.DefaultClient._list(self, **kwargs)

    def normalize(self, str_in: str, *args):
        return str_in.replace('-','').replace('_','').lower()
 
    def create(self, params: dict = None, **kwargs) -> 'DefaultResource':
        LOG.info(self._log_message("[CREATE] Create CRD new ", body=params, args=kwargs))
        if self.__class__.__name__ == 'Services':
            params['name'] = self.normalize(params['name'])
            spec = copy.deepcopy(resources.Service.SPEC)
            spec['metadata']['namespace'] = self.crd_client.ocp_namespace
            spec['metadata']['name'] = params['name']
            spec['spec']['providerAccountRef']['name'] = self.crd_client.ocp_provider_ref
            for k,v in resources.Service.KEYS.items():
                if params.get(k, None):
                    spec['spec'][resources.Service.KEYS[k]] = params[k]
                else:
                    del(spec['spec'][resources.Service.KEYS[k]])
            result = ocp.create(spec)
            assert result.status() == 0
            
            list_objs = self.read_crd(self._entity_collection, result.out().strip().split('/')[1])
            return (self._create_instance(response=list_objs)[:1] or [None])[0]
            
        return threescale_api.defaults.DefaultClient.create(self, params, **kwargs)


    def _create_instance(self, response, klass=None, collection: bool = False):
        klass = klass or self._instance_klass
        if self.__class__.__name__ == 'Services':
            extracted = self._extract_resource_crd(response, collection)
            instance = self._instantiate_crd(extracted=extracted, klass=klass)
        else:
            extracted = self._extract_resource(response, collection)
            instance = self._instantiate(extracted=extracted, klass=klass)
        LOG.debug(f"[INSTANCE] Created instance: {instance}")
        return instance

    def _extract_resource_crd(self, response, collection) -> Union[List, Dict]:
        extract_params = dict(response=response, entity=self._entity_name)
        if collection:
            extract_params['collection'] = self._entity_collection
        extracted = None
        #if collection and collection in extracted:
        #    extracted = extracted.get(collection)
        if isinstance(response, list):
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
        instance = klass(client=self, **extracted) if klass else extracted
        return instance


    def delete(self, entity_id: int = None, resource: 'DefaultResource' = None, **kwargs) -> bool:
        LOG.info(self._log_message("[DELETE] Delete CRD ", entity_id=entity_id, args=kwargs))
        if self.__class__.__name__ == 'Services':
            resource.crd.delete()
        return threescale_api.defaults.DefaultClient.delete(self, entity_id=entity_id, **kwargs)

    
    def update(self, entity_id=None, params: dict = None, resource: 'DefaultResource' = None, **kwargs) -> 'DefaultResource':
        LOG.info(self._log_message("[UPDATE] Update CRD", body=params,
                                   entity_id=entity_id, args=kwargs))

        if self._instance_klass.__name__ == 'Service':
            # Safer way than using only apply()
            def _modify(apiobj):
                for key in apiobj.model.spec.keys():
                    if key in resources.Service.KEYS:
                        apiobj.model.spec[key] = resource.entity[key]
    
            result, success = resource.crd.modify_and_apply(modifier_func=_modify)
            if not success:
                LOG.error(f"[INSTANCE] Update failed: {result}")
            return resource.read()

        return threescale_api.defaults.DefaultClient.update(self, entity_id=entity_id, params=params, **kwargs)

        
        #instance = self._create_instance(response=response)
        #return instance



class DefaultResourceCRD(threescale_api.defaults.DefaultResource):
    def __init__(self, crd = None, *args, **kwargs):
        threescale_api.defaults.DefaultResource.__init__(self, *args, **kwargs)
        self._crd = crd
    
    @property
    def crd(self):
        return self._crd
