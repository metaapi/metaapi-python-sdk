Token Management API
####################
Generating token to use in Web or Mobile applications
=====================================================
A typical admin token generated with `MetaApi Web application <https://app.metaapi.cloud/generate-token>`_ is usually allowed to access all MetaApi resources. Thus such token might be unsafe to be used in a web or mobile app, because a user can capture the token from the application and then be able to perform unwanted actions on his own. We introduced token management api to SDK so that you can create new token that would be safe to use in your Web or Mobile applications. This is achieved by narrowing down permissions of your admin token.
There are 2 styles of this API - simplified and detailed.

Simplified TokenManagement API
------------------------------
Simplified API let you to narrow down token permissions using simple methods without specifying full access rules which might be complicated to formulate in your app.

Narrow down access to specific applications only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To narrow down access to specific applications only please use narrow_down_token_applications method. You can specify token validity period. Default is 24 (hours).

.. code-block:: python

    try: 
        # restrict web app token with access to Trading account management API and MetaStats API only
        narrowed_down_token = await api.token_management_api.narrow_down_token_applications(
            ['trading-account-management-api', 'metastats-api'], 
            validity_in_hours
        )
    except Exception as err:
        print(err)
    

Narrow down token permissions to specific roles only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to narrow down token permissions to specific roles please use narrow_down_token_roles method. You can specify token validity period. Default is 24 (hours).

.. code-block:: python

    try:
        # restrict web app token with read-only access
        narrowed_down_token = await api.token_management_api.narrow_down_token_roles(
            ['reader'], 
            validity_in_hours
        )
    except Exception as err:
        print(err)


Narrow down token permissions to access specific resources only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to narrow down token permissions to access specific resources please use method narrow_down_token_resources. You can specify token validity period. Default is 24 (hours).

.. code-block:: python

    try:
        # restrice web app token to access specific trading account only
        narrowed_down_token = await api.token_management_api.narrow_down_token_resources(
            [{'entity': 'account', 'id': '3860c395-6842-43d9-9b6a-9f9841bb2c8a'}],
            validity_in_hours
        )
    except Exception as err:
        print(err)



Narrow down access specific applications, resources and roles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using the same simplified API you can combine 3 options listed above to restrict token access to applications, resources and/or roles. You can also specify token validity period. Default is 24 (hours).

.. code-block:: python

    try {
        # restrict web app token with read-only access for MetaApi REST API for specific trading account only
        narrowed_down_token = await api.token_management_api.narrow_down_token(
            {
                'applications': ['metaapi-api'],
                'roles': ['reader'],
                'resources': [{'entity': 'account', 'id': '3860c395-6842-43d9-9b6a-9f9841bb2c8a'}]
            }, 
            validity_in_hours
        )
    except Exception as err:
        print(err)



Detailed token management API
-----------------------------
Using the narrow_down_token method you can specify detailed access rules you need for token. You can also specify token validity period. Default is 24 (hours).

.. code-block:: python

    # generate a token with access rules specified in detailed format
    narrowed_down_token = await api.token_management_api.narrow_down_token(
        {
            'accessRules': [
                {
                    'id': 'trading-account-management-api',
                    'application': 'trading-account-management-api',
                    'service': 'rest',
                    'resources': [{'entity': 'account', 'id': '3860c395-6842-43d9-9b6a-9f9841bb2c8a'}],
                    'methodGroups': [{'group': 'account-management', 'methods': [{'method': 'getAccount'}]}],
                    'roles': ['reader']
                },
                {
                    'id': 'mt-manager-api',
                    'application': 'mt-manager-api',
                    'service': 'rest',
                    'resources': [{'entity': 'mt-manager', 'id': 'c55da8ff-c177-4236-bf4c-a832a67c6ab3'}],
                    'methodGroups': [{'group': '*', 'methods': [{'method': '*', 'scopes': ['dealing', 'public']}]}],
                    'roles': ['reader']
                }
            ],
        },
        validity_in_hours
    )


Get Access Rules Manifest
-------------------------
To get full list of available access rule elements for detailed token management API you can use get_access_rules method

.. code-block:: python

    manifest = await api.token_management_api.get_access_rules()


Check if token is narrowed down
-------------------------------
You can check if token is narrowed down using are_token_resources_narrowed_down method. Note that this method only checks if resource access is restricted. It lacks understanding about your security context and use cases so that it can not tell you if your token is indeed safe to be used in your use case. You can rely on this method only as an extra precautionary check. We recommend you to carefully test your code to make sure that tokens you generate are safe to be used in your web and mobile apps.

.. code-block:: python

    are_resources_narrowed_down = api.token_management_api.are_token_resources_narrowed_down(token)

