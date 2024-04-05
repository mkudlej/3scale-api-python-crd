def test_policies_append(proxy):
    policies = proxy.policies.list()
    policy_1 = {
        "name": "logging",
        "configuration": {},
        "version": "builtin",
        "enabled": True,
    }
    proxy.policies.append(policy_1)
    policies["policies_config"].append(policy_1)
    updated_policies = proxy.policies.list()
    for pol1, pol2 in zip(
        policies["policies_config"], updated_policies["policies_config"]
    ):
        if hasattr(pol1, "entity"):
            pol1 = pol1.entity
        for attr in ["service_id", "id"]:
            if attr in pol1:
                pol1.pop(attr)

        if hasattr(pol2, "entity"):
            pol2 = pol2.entity
        for attr in ["service_id", "id"]:
            if attr in pol2:
                pol2.pop(attr)

        assert pol1 == pol2


def test_policies_insert(proxy):
    policies = proxy.policies.list()
    policy_2 = {
        "name": "echo",
        "configuration": {},
        "version": "builtin",
        "enabled": True,
    }
    proxy.policies.insert(1, policy_2)
    policies["policies_config"].insert(1, policy_2)
    updated_policies = proxy.policies.list()
    for pol1, pol2 in zip(
        policies["policies_config"], updated_policies["policies_config"]
    ):
        if hasattr(pol1, "entity"):
            pol1 = pol1.entity
        for attr in ["service_id", "id"]:
            if attr in pol1:
                pol1.pop(attr)

        if hasattr(pol2, "entity"):
            pol2 = pol2.entity
        for attr in ["service_id", "id"]:
            if attr in pol2:
                pol2.pop(attr)

        assert pol1 == pol2
