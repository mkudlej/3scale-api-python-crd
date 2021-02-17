"""
Module with constants.
"""

SERVICE_AUTH = {
    'userkey': '1',
    'appKeyAppID': '2',
    'oidc': 'oidc'
    }

SPEC_SERVICE = {
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
                'authentication': {
                    'userkey': {
                        'authUserKey': 'token',
                        'credentials': 'query',
                        },
                    },
                },
            },
        'applicationPlans': {
            'AppPlanTest': {
                'setupFee': '10.70',
                'costMonth': '10.80',
                }
            },
        },
    }

SPEC_BACKEND = {
    'apiVersion': 'capabilities.3scale.net/v1beta1',
    'kind': 'Backend',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'spec': {
        'name': None,
        'privateBaseURL': None,
        'systemName': None,
        'providerAccountRef': {
            'name': None,
            },
        'description': None
        },
    }

SPEC_MAPPING_RULE = {
    'spec': {
        'httpMethod': None,
        'pattern': None,
        'increment': None,
        'metricMethodRef': None,
        'last': None
        }
    }

SPEC_BACKEND_USAGE = {
    'spec': {
        'path': None,
        }
    }

SPEC_METRIC = {
    'spec': {
        'friendlyName': None,
        'unit': None,
        'description': None,
        }
    }
SPEC_APP_PLANS = {
    'spec': {
        'name': None,
        'appsRequireApproval': None,
        'trialPeriod': None,
        'setupFee': None,
        'costMonth': None,
        # TODO pricingRules
        # TODO limits
        }
    }

SPEC_ACTIVE_DOC = {
    'apiVersion': 'capabilities.3scale.net/v1beta1',
    'kind': 'ActiveDoc',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'spec': {
        'name': None,
        'providerAccountRef': {
            'name': None,
            },
        'activeDocOpenAPIRef': {
            'secretRef': 'oas3-json-secret',
            },
        'systemName': None,
        'description': None,
        'productSystemName': None,
        'published': False,
        'skipSwaggerValidations': False
    }
}

SPEC_POLICY_REG = {
    'apiVersion': 'capabilities.3scale.net/v1beta1',
    'kind': 'Policy',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'spec': {
        'name': None,
        'providerAccountRef': {
            'name': None,
            },
        'version': None,
        'schema': {
            'name': None,
            'version': None,
            'summary': None,
            '$schema': None,
            'description': None,
            'configuration': None
            }
    }
}
KEYS_SERVICE = {
    'description': 'description',
    'name': 'name',
    'system_name': 'systemName',
    'mapping_rules': 'mappingRules',
    'metrics': 'metrics',
    'backend_usages': 'backendUsages'
}

KEYS_BACKEND = {
    'description': 'description',
    'name': 'name',
    'system_name': 'systemName',
    'mapping_rules': 'mappingRules',
    'private_endpoint': 'privateBaseURL',
    'metrics': 'metrics'
}
KEYS_MAPPING_RULE = {
    'http_method': 'httpMethod',
    'pattern': 'pattern',
    'delta': 'increment',
    'metric_id': 'metricMethodRef',
    'last': 'last'
}
KEYS_ACTIVE_DOC = {
    'system_name': 'systemName',
    'name': 'name',
    'description': 'description',
    'published': 'published',
    'skip_swagger_validations': 'skipSwaggerValidations',
    'service_id': 'productSystemName',
    # because of modify function for update
    'activeDocOpenAPIRef': 'activeDocOpenAPIRef'
}

KEYS_POLICY_REG = {
    'name': 'name',
    'version': 'version',
    'schema': 'schema',
    'summary': 'summary',
    '$schema': '$schema',
    'description': 'description',
    'configuration': 'configuration'
}

KEYS_METRIC = {
    'description': 'description',
    'unit': 'unit',
    'friendly_name': 'friendlyName',
    'name': 'name'
}

KEYS_APP_PLANS = {
    'name': 'name',
    'approval_required': 'appsRequireApproval',
    'trial_period_days': 'trialPeriod',
    'setup_fee': 'setupFee',
    'cost_per_month': 'costMonth',
    'system_name': 'system_name',
    # missing state, cancellation_period, default, custom
}

KEYS_BACKEND_USAGE = {
    'path': 'path',
    'service_id': 'service_id',
    'backend_id': 'backend_id',
}

SPEC_SECRET = {
    'kind': 'Secret',
    'apiVersion': 'v1',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'data': {},
    'type': 'Opaque'
}
