# 3scale-api-python-crd

### Integration tests configuration

To run the integration tests you need to set these env variables:
```
THREESCALE_PROVIDER_URL='https://example-admin.3scale.net'
THREESCALE_PROVIDER_TOKEN='<test-token>'
OCP_PROVIDER_ACCOUNT_REF='threescale-provider-account'

# OPTIONAL:
THREESCALE_MASTER_URL='https://master.3scale.net'
THREESCALE_MASTER_TOKEN='<test-master-token>'
```

and to have valid `oc` tool session.

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

Command to run integration unit tests: `pipenv run pytest --log-cli-level=10 -vvvv -s ./tests/integration/test_integration_activedocs.py ./tests/integration/test_integration_services.py ./tests/integration/test_integration_backends.py ./tests/integration/test_integration_policy_registry.py ./tests/integration/test_integration_application_plan.py ./tests/integration/test_integration_policies.py ./tests/integration/test_integration_accounts.py ./tests/integration/test_integration_backend_mapping_rules.py ./tests/integration/test_integration_custom_tenant.py ./tests/integration/test_integration_limit.py ./tests/integration/test_integration_pricing_rules.py ./tests/integration/test_integration_promotes.py |& tee f`
 
### TODO

- add tests for promoting promotes

- add system-seed support

- fix tests/integration/test_integration_mapping_rules.py::test_should_update_mapping_rule

- add disabling CRD - self.client.CRD_IMPLEMENTED = False is wrong
- create unit integration tests for:
  - Application
  - methods
  - ProductDeploymentSpec
  - AuthenticationSpec

- create jenkins job for running unit tests
- add proper delete tests to all above unit tests - check if there is one less entity after delete
- add proper error messages in case of for example missing required arguments, see test_should_fields_be_required 
- implement optimitazation on the oc level:
  - for every test run, label objects - oc label product.capabilities.3scale.net/testyrclkfzyhue test_run=new --overwrite
  - use only objects labeled by test run id - oc get product.capabilities.3scale.net --show-labels=true -l test_run=new
- add support for Methods
