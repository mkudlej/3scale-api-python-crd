from tests.integration import asserts

# tests important for CRD - CRU + list


def test_accounts_list(api, account, acc_user):
    accounts = api.accounts.list()
    assert len(accounts) >= 1


def test_account_can_be_created(api, account, account_params, acc_user):
    asserts.assert_resource(account)
    asserts.assert_resource_params(account, account_params)


def test_account_can_be_read(api, account, account_params, acc_user):
    read = api.accounts.read(account.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)


def test_account_can_be_read_by_name(api, account, account_params, acc_user):
    account_name = account["org_name"]
    read = api.accounts[account_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)


def test_account_can_be_updated(api, account, acc_user):
    account["monthly_charging_enabled"] = True
    acc_updated = account.update()
    assert (
        account["monthly_charging_enabled"]
        == True
        == acc_updated["monthly_charging_enabled"]
    )
    updated = account.read()
    assert (
        updated["monthly_charging_enabled"]
        == True
        == account["monthly_charging_enabled"]
    )


# end of tests important for CRD - CRU + list

# tests important for CRD - CRU + list


def test_users_list(api, account, acc_user):
    users = account.users.list()
    assert len(users) >= 1
    users = api.account_users.list()
    assert len(users) >= 1


def test_user_can_be_created(
    api, account, account_params, acc_user, acc_user2, acc_user2_params
):
    asserts.assert_resource(acc_user)
    asserts.assert_resource_params(acc_user, account_params)

    asserts.assert_resource(acc_user2)
    asserts.assert_resource_params(acc_user2, acc_user2_params)


def test_user_can_be_read(api, account, account_params, acc_user):
    read = account.users.read(acc_user.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)

    read = api.account_users.read(acc_user.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)


def test_user_can_be_read_by_name(api, account, account_params, acc_user):
    user_name = acc_user["username"]
    read = account.users[user_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)

    read = api.account_users[user_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)


def test_user_can_be_updated(api, account, acc_user2):
    acc_user2["role"] = "admin"
    user2_updated = acc_user2.update()
    assert acc_user2["role"] == "admin" == user2_updated["role"]
    updated = acc_user2.read()
    assert updated["role"] == "admin" == acc_user2["role"]


# end of tests important for CRD - CRU + list

# TODO - implement and create unit tests for user states and permissions
