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
                'published': True,
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
        'publish': True,
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

#           'openapiRef': {
#            'url': None,
#            },
#        'productionPublicBaseURL': None,
#        'stagingPublicBaseURL': None,
#        'productSystemName': None,
#        'privateBaseURL': None,
#        'prefixMatching': None,
#        'privateAPIHostHeader': None,
#        'privateAPISecretToken': None

SPEC_OPEN_API = {
    'apiVersion': 'capabilities.3scale.net/v1beta1',
    'kind': 'OpenAPI',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'spec': {
        'providerAccountRef': {
            'name': None,
            },
    }
}

SPEC_TENANT = {
    'apiVersion': 'capabilities.3scale.net/v1alpha1',
    'kind': 'Tenant',
    'metadata': {
        'name': None,
        'namespace': None,
        },
    'spec': {
        'organizationName': None,
        'email': None,
        'username': None,
        'systemMasterUrl': None,
        'masterCredentialsRef': {
            'name': None,
            },
        'passwordCredentialsRef': {
            'name': None,
            },
        'tenantSecretRef': {
            'name': None,
            'namespace': None
            }
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

KEYS_PROXY_RESPONSES = {
    'error_auth_failed': 'errorAuthFailed',
    'error_auth_missing': 'errorAuthMissing',
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

KEYS_PROXY_RESPONSES = {
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

KEYS_PROXY_SECURITY = {
    'secret_token': 'secretToken',
    'host_header': 'hostHeader',
    }

KEYS_PROXY = {
    'credentials_location': 'credentials',
    'endpoint': 'productionPublicBaseURL',
    'sandbox_endpoint': 'stagingPublicBaseURL',
    'auth_user_key': 'authUserKey',
    'auth_app_key': 'appKey',
    'auth_app_id': 'appID',
    'oidc_issuer_endpoint': 'issuerEndpoint',
    'oidc_issuer_type': 'issuerType',
    'jwt_claim_with_client_id': 'jwtClaimWithClientID',
    'jwt_claim_with_client_id_type': 'jwtClaimWithClientIDType',
        }

KEYS_OIDC = {
    'standard_flow_enabled': 'standardFlowEnabled',
    'implicit_flow_enabled': 'implicitFlowEnabled',
    'service_accounts_enabled': 'serviceAccountsEnabled',
    'direct_access_grants_enabled': 'directAccessGrantsEnabled',
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
    'publish': 'published',
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

KEYS_OPEN_API = {
    'productionPublicBaseURL': 'productionPublicBaseURL',
    'stagingPublicBaseURL': 'stagingPublicBaseURL',
    'productSystemName': 'productSystemName',
    'privateBaseURL': 'privateBaseURL',
    'prefixMatching': 'prefixMatching',
    'privateAPIHostHeader': 'privateAPIHostHeader',
    'privateAPISecretToken': 'privateAPISecretToken'
}

KEYS_TENANT = {
    'org_name': 'organizationName',
    'support_email': 'email',
    'username': 'username',
    'system_master_url': 'systemMasterUrl',
    'tenantSecretRef': 'tenantSecretRef'
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
