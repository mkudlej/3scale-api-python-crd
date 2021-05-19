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
                        'gatewayResponse': {
                            },
                        },
                    },
                },
            },
        'applicationPlans': {
            'AppPlanTest': {
                'setupFee': '0.00',
                'costMonth': '0.00',
                }
            },
        },
        'policies': [] 
    }

SPEC_PROXY = {}


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
    'kind': 'CustomPolicyDefinition',
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


SPEC_ACCOUNT = {
    'apiVersion': 'capabilities.3scale.net/v1beta1',
    'kind': 'DeveloperAccount',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'spec': {
        'providerAccountRef': {
            'name': None,
            },
        'orgName': None,
        'monthlyBillingEnabled': None,
        'monthlyChargingEnabled': None
    }
}

SPEC_ACCOUNT_USER = {
    'apiVersion': 'capabilities.3scale.net/v1beta1',
    'kind': 'DeveloperUser',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'spec': {
        'providerAccountRef': {
            'name': None,
            },
        'username': None,
        'email': None,
        'suspended': None,
        'role': None,
        'passwordCredentialsRef': {
            'name': None,
        },
        'developerAccountRef': {
            'name': None,
        }
    }
}

SPEC_POLICY = {
    'spec': {
        'name': None,
        'version': None,
        'enabled': None,
        'configuration': {},
        }
    }

KEYS_SERVICE = {
    'description': 'description',
    'name': 'name',
    'system_name': 'systemName',
    'mapping_rules': 'mappingRules',
    'metrics': 'metrics',
    'backend_usages': 'backendUsages',
    'application_plans': 'applicationPlans',
    'deployment': 'deployment',
    'policies': 'policies',
}

KEYS_PROXY = {
    'error_auth_failed': 'errorAuthFailed',
    'error_auth_missing': 'errorAuthMissing',
    'error_headers_auth_failed': 'errorHeadersAuthFailed',
    'error_headers_auth_missing': 'errorHeadersAuthMissing',
    'error_headers_limits_exceeded': 'errorHeadersLimitsExceeded',
    'error_headers_no_match': 'errorHeadersNoMatch',
    'error_limits_exceeded': 'errorLimitsExceeded',
    'error_no_match': 'errorNoMatch',
    'error_status_auth_failed': 'errorStatusAuthFailed',
    'error_status_auth_missing': 'errorStatusAuthMissing',
    'error_status_limits_exceeded': 'errorStatusLimitsExceeded',
    'error_status_no_match': 'errorStatusNoMatch',
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
    # missing state, cancellation_period, default, custom
}

KEYS_BACKEND_USAGE = {
    'path': 'path',
    'service_id': 'service_id',
    'backend_id': 'backend_id',
}

KEYS_ACCOUNT = {
    'org_name': 'orgName',
    'monthly_billing_enabled': 'monthlyBillingEnabled',
    'monthly_charging_enabled': 'monthlyChargingEnabled'
    # missing credit_card_stored, created_at, updated_at
}

KEYS_ACCOUNT_USER = {
    'username': 'username',
    'email': 'email',
    'suspended': 'suspended',
    'role': 'role'
}

KEYS_POLICY = {
    'name': 'name',
    'version': 'version',
    'configuration': 'configuration',
    'enabled': 'enabled',
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
