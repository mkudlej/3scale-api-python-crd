# 3scale-api-python-crd

### Integration tests configuration

To run the integration tests you need to set these env variables:
```
THREESCALE_PROVIDER_URL='https://example-admin.3scale.net'
THREESCALE_PROVIDER_TOKEN='<test-token>'

THREESCALE_MASTER_URL='https://master.3scale.net'
THREESCALE_MASTER_TOKEN='<test-master-token>'
```

and to have valid `oc` tool session.

By default:
    - `oc` namespace should be the namespace where 3scale instance is deployed
    - the `system-seed` secret is used by 3scale Operator client
    - `THREESCALE_` variables are used for not implemented Threescale client features

If CRDs are created in different namespace to 3scale deployment, env variable 
`OCP_PROVIDER_ACCOUNT_REF` can be specified with secret name used by 3scale Operator client,
see https://github.com/3scale/3scale-operator/blob/master/doc/backend-reference.md#provider-account-reference

### Finished integration unit tests

- AccountUsers
- Accounts
- ActiveDocs
- ApplicationPlans
- BackendMappingRules
- BackendMetrics
- BackendUsages
- Backends
- Limits
- MappingRules
- Metrics
- OpenApis
- Policies
- PolicyRegistries
- PricingRules
- Proxies
- Services
- Tenants
- ProxyConfigPromote
- Applications

Command to run integration unit tests: `pipenv run pytest --log-cli-level=10 -vvvv -s ./tests/integration/test_integration_activedocs.py ./tests/integration/test_integration_services.py ./tests/integration/test_integration_backends.py ./tests/integration/test_integration_policy_registry.py ./tests/integration/test_integration_application_plan.py ./tests/integration/test_integration_policies.py ./tests/integration/test_integration_accounts.py ./tests/integration/test_integration_backend_mapping_rules.py ./tests/integration/test_integration_custom_tenant.py ./tests/integration/test_integration_limit.py ./tests/integration/test_integration_pricing_rules.py ./tests/integration/test_integration_promotes.py ./tests/integration/test_integration_application.py |& tee f`
 
### TODO
- add disabling CRD - self.client.CRD_IMPLEMENTED = False is wrong
- create unit integration tests for:
  - methods
  - ProductDeploymentSpec
  - AuthenticationSpec
- add support of different namespaces

- create jenkins job for running unit tests
- add proper error messages in case of for example missing required arguments, see test_should_fields_be_required 
- implement optimitazation on the oc level:
  - for every test run, label objects - oc label product.capabilities.3scale.net/testyrclkfzyhue test_run=new --overwrite
  - use only objects labeled by test run id - oc get product.capabilities.3scale.net --show-labels=true -l test_run=new
- add support for Methods
