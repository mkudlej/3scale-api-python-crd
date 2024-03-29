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
- Methods

Command to run integration unit tests: `pipenv run pytest --log-cli-level=10 -vvvv -s ./tests/integration/ |& tee x`
 
### TODO
- do https://github.com/3scale/3scale-operator/pull/813
- do not simulate app plan id
- create unit integration tests for:
  - ProductDeploymentSpec
  - AuthenticationSpec
- implement delete of policies + add unit tests
- create jenkins job for running unit tests
- add proper error messages in case of for example missing required arguments, see test_should_fields_be_required 
- implement optimitazation on the oc level:
  - for every test run, label objects - oc label product.capabilities.3scale.net/testyrclkfzyhue test_run=new --overwrite
  - use only objects labeled by test run id - oc get product.capabilities.3scale.net --show-labels=true -l test_run=new
