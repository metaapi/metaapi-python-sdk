Managing MetaTrader accounts and provisioning profiles
######################################################

Managing MetaTrader accounts (API servers for MT accounts)
==========================================================
Before you can use the API you have to add an MT account to MetaApi and start an API server for it.

Managing MetaTrader accounts (API servers) via web UI
-----------------------------------------------------
You can manage MetaTrader accounts here: https://app.metaapi.cloud/accounts

Create a MetaTrader account (API server) via API
------------------------------------------------

Creating an account using automatic broker settings detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create an account, supply a request with account data and the platform field indicating the MetaTrader version.
Provisioning profile id must not be included in the request for automatic broker settings detection.

.. code-block:: python

    try:
        account = await api.metatrader_account_api.create_account(account={
          'name': 'Trading account #1',
          'type': 'cloud',
          'login': '1234567',
          'platform': 'mt4',
          # password can be investor password for read-only access
          'password': 'qwerty',
          'server': 'ICMarketsSC-Demo',
          'magic': 123456,
          'keywords': ["Raw Trading Ltd"],
          'quoteStreamingIntervalInSeconds': 2.5, # set to 0 to receive quote per tick
          'reliability': 'high' # set this field to 'high' value if you want to increase uptime of your account (recommended for production environments)
        })
    except Exception as err:
        # process errors
        if hasattr(err, 'details'):
            # returned if the server file for the specified server name has not been found
            # recommended to check the server name or create the account using a provisioning profile
            if err.details == 'E_SRV_NOT_FOUND':
                print(err)
            # returned if the server has failed to connect to the broker using your credentials
            # recommended to check your login and password
            elif err.details == 'E_AUTH':
                print(err)
            # returned if the server has failed to detect the broker settings
            # recommended to try again later or create the account using a provisioning profile
            elif err.details == 'E_SERVER_TIMEZONE':
                print(err)

Broker settings detection or connection validation might take some time. If so you will receive response with request processing stage and wait time:

.. code-block:: python

    Retrying request in 60 seconds because request returned message: Automatic broker settings detection is in progress, please retry in 60 seconds

The client will automatically retry the request when the recommended time passes.

Error handling
^^^^^^^^^^^^^^
Several types of errors are possible during the request:

- Server file not found
- Authentication error
- Settings detection error

Server file not found
"""""""""""""""""""""
This error is returned if the server file for the specified server name has not been found. In case of this error it
is recommended to check the server name. If the issue persists, it is recommended to create the account using a
provisioning profile.

.. code-block:: python

    {
        "id": 3,
        "error": "ValidationError",
        "message": "We were unable to retrieve the server file for this broker. Please check the server name or configure the provisioning profile manually.",
        "details": "E_SRV_NOT_FOUND"
    }

Authentication error
""""""""""""""""""""
This error is returned if the server has failed to connect to the broker using your credentials. In case of this
error it is recommended to check your login and password, and try again.

.. code-block:: python

    {
        "id": 3,
        "error": "ValidationError",
        "message": "We failed to authenticate to your broker using credentials provided. Please check that your MetaTrader login, password and server name are correct.",
        "details": "E_AUTH"
    }

Settings detection error
""""""""""""""""""""""""
This error is returned if the server has failed to detect the broker settings. In case of this error it is recommended
to retry the request later, or create the account using a provisioning profile.

.. code-block:: python

    {
        "id": 3,
        "error": "ValidationError",
        "message": "We were not able to retrieve server settings using credentials provided. Please try again later or configure the provisioning profile manually.",
        "details": "E_SERVER_TIMEZONE"
    }

Creating an account using a provisioning profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If creating the account with automatic broker settings detection has failed, you can create it using a `provisioning profile. <#managing-provisioning-profiles>`_
To create an account using a provisioning profile, create a provisioning profile for the MetaTrader server, and then add the provisioningProfileId field to the request:

.. code-block:: python

    account = await api.metatrader_account_api.create_account(account={
      'name': 'Trading account #1',
      'type': 'cloud',
      'login': '1234567',
      # password can be investor password for read-only access
      'password': 'qwerty',
      'server': 'ICMarketsSC-Demo',
      'provisioningProfileId': provisioningProfile.id,
      'magic': 123456,
      'quoteStreamingIntervalInSeconds': 2.5, # set to 0 to receive quote per tick
      'reliability': 'high' # set this field to 'high' value if you want to increase uptime of your account (recommended for production environments)
    })

Account configuration by end user
------------------------------------
MetaApi supports trading account configuration by end user. If you do not specify trading account login and password in the createAccount method payload the account will be created in a DRAFT state. You then can generate a link your user can use to enter account login and password or change the account password.

.. code-block:: python

    account = await api.metatrader_account_api.create_account(account={
      'name': 'Trading account #1',
      'type': 'cloud',
      'server': 'ICMarketsSC-Demo',
      'provisioningProfileId': provisioningProfile.id,
      'application': 'MetaApi',
      'magic': 123456,
      'quoteStreamingIntervalInSeconds': 2.5, # set to 0 to receive quote per tick
      'reliability': 'high' # set this field to 'high' value if you want to increase uptime of your account (recommended for production environments)
    })
    configuration_link = await account.create_configuration_link(ttl_in_days=7)

Retrieving existing accounts via API
------------------------------------

Method ``get_accounts_with_infinite_scroll_pagination`` provides pagination in a classic style which allows you to calculate page count.

.. code-block:: python

    # filter and paginate accounts, see doc for full list of filter options available
    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination(accounts_filter={
        'limit': 10,
        'offset': 0,
        'query': 'ICMarketsSC-MT5',
        'state': ['DEPLOYED']
    })

    # get accounts without filter (returns 1000 accounts max)
    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
    account = None

    for acc in accounts['items']]:
      if acc.id == 'accountId':
        account = acc
        break

Method ``get_accounts_with_classic_scroll_pagination`` provides pagination in a classic style which allows you to calculate page count.

.. code-block:: python

    # filter and paginate accounts, see doc for full list of filter options available
    accounts = await api.metatrader_account_api.get_accounts_with_classic_scroll_pagination(accounts_filter={
        'limit': 10,
        'offset': 0,
        'query': 'ICMarketsSC-MT5',
        'state': ['DEPLOYED']
    })
    account = None

    for acc in accounts['items']]:
      if acc.id == 'accountId':
        account = acc
        break
    # number of all accounts matching filter without pagination options
    print(accounts['count'])
    # get accounts without filter (returns 1000 accounts max)
    accounts = await api.metatrader_account_api.get_accounts_with_classic_scroll_pagination();

Method ``get_account`` retrieves account by account id.

.. code-block:: python

    account = await api.metatrader_account_api.get_account('accountId')

Updating an existing account via API
------------------------------------
.. code-block:: python

    await account.update(account={
        'name': 'Trading account #1',
        'login': '1234567',
        # password can be investor password for read-only access
        'password': 'qwerty',
        'server': 'ICMarketsSC-Demo',
        'quoteStreamingIntervalInSeconds': 2.5
    })

Removing an account
-------------------
.. code-block:: python

    await account.remove()

Deploying, undeploying and redeploying an account (API server) via API
----------------------------------------------------------------------
.. code-block:: python

    await account.deploy()
    await account.undeploy()
    await account.redeploy()

Manage custom experts (EAs)
---------------------------
Custom expert advisors can only be used for MT4 accounts on g1 infrastructure. EAs which use DLLs are not supported.

Creating an expert advisor via API
----------------------------------
You can use the code below to create an EA. Please note that preset field is a base64-encoded preset file.

.. code-block:: python

    expert = await account.create_expert_advisor(expert_id='expertId', expert={
        'period': '1h',
        'symbol': 'EURUSD',
        'preset': 'a2V5MT12YWx1ZTEKa2V5Mj12YWx1ZTIKa2V5Mz12YWx1ZTMKc3VwZXI9dHJ1ZQ'
    })
    await expert.upload_file('/path/to/custom-ea')

Retrieving existing experts via API
-----------------------------------

.. code-block:: python

    experts = await account.get_expert_advisors()

Retrieving existing expert by id via API
----------------------------------------

.. code-block:: python

    expert = await account.get_expert_advisor(expert_id='expertId')

Updating existing expert via API
--------------------------------
You can use the code below to update an EA. Please note that preset field is a base64-encoded preset file.

.. code-block:: python

    await expert.update(expert={
        'period': '4h',
        'symbol': 'EURUSD',
        'preset': 'a2V5MT12YWx1ZTEKa2V5Mj12YWx1ZTIKa2V5Mz12YWx1ZTMKc3VwZXI9dHJ1ZQ'
    })
    await expert.upload_file('/path/to/custom-ea')

Removing expert via API
-----------------------

.. code-block:: python

    await expert.remove()

Managing provisioning profiles
==============================
Provisioning profiles can be used as an alternative way to create MetaTrader accounts if the automatic broker settings
detection has failed.

Managing provisioning profiles via web UI
-----------------------------------------
You can manage provisioning profiles here: https://app.metaapi.cloud/provisioning-profiles

Creating a provisioning profile via API
---------------------------------------
.. code-block:: python

    # if you do not have created a provisioning profile for your broker,
    # you should do it before creating an account
    provisioningProfile = await api.provisioning_profile_api.create_provisioning_profile(profile={
        'name': 'My profile',
        'version': 5,
        'brokerTimezone': 'EET',
        'brokerDSTSwitchTimezone': 'EET'
    })
    # servers.dat file is required for MT5 profile and can be found inside
    # config directory of your MetaTrader terminal data folder. It contains
    # information about available broker servers
    await provisioningProfile.upload_file(file_name='servers.dat', file='/path/to/servers.dat')
    # for MT4, you should upload an .srv file instead
    await provisioningProfile.upload_file(file_name='broker.srv', file='/path/to/broker.srv')

Retrieving existing provisioning profiles via API
-------------------------------------------------

Method ``get_provisioning_profiles_with_infinite_scroll_pagination`` provides pagination in infinite scroll style.

.. code-block:: python

    # filter and paginate profiles, see doc for full list of filter options available
    provisioningProfiles = await api.provisioning_profile_api.get_provisioning_profiles_with_infinite_scroll_pagination({
        'limit': 10,
        'offset': 0,
        'query': 'ICMarketsSC-MT5', # searches over name
        'version': 5
    })

    # get profiles without filter (returns 1000 profiles max)
    provisioningProfiles = await api.provisioning_profile_api.get_provisioning_profiles_with_infinite_scroll_pagination()
    provisioningProfile = None

    for profile in provisioningProfiles:
        if profile.id == 'profileId':
          provisioningProfile = profile
          break

Method ``get_provisioning_profiles_with_classic_pagination`` provides pagination in a classic style which allows you to calculate page count.

.. code-block:: python

    # filter and paginate profiles, see doc for full list of filter options available
    provisioningProfiles = await api.provisioning_profile_api.get_provisioning_profiles_with_classic_pagination({
        'limit': 10,
        'offset': 0,
        'query': 'ICMarketsSC-MT5', # searches over name
        'version': 5
    })
    provisioningProfile = None

    for profile in provisioningProfiles['items']:
        if profile.id == 'profileId':
          provisioningProfile = profile
          break

    # number of all profiles matching filter without pagination options
    print(provisioningProfiles['count'])

    # get profiles without filter (returns 1000 profiles max)
    provisioningProfiles = await api.provisioning_profile_api.get_provisioning_profiles_with_classic_pagination()

Method ``get_provisioning_profile`` retrieves profile by profile id.

.. code-block:: python

    provisioningProfile = await api.provisioning_profile_api.get_provisioning_profile('profileId')

Updating a provisioning profile via API
---------------------------------------
.. code-block:: python

    await provisioningProfile.update(profile={'name': 'New name'})
    # for MT5, you should upload a servers.dat file
    await provisioningProfile.upload_file(file_name='servers.dat', file='/path/to/servers.dat')
    # for MT4, you should upload an .srv file instead
    await provisioningProfile.upload_file(file_name='broker.srv', file='/path/to/broker.srv')

Removing a provisioning profile
-------------------------------
.. code-block:: python

    await provisioningProfile.remove()

Managing MetaTrader accounts via API
=========================================
Please note that not all MT4/MT5 servers allows you to create demo accounts using the method below.

Create a MetaTrader 4 demo account
----------------------------------
.. code-block:: python

    demo_account = await api.metatrader_account_generator_api.create_mt4_demo_account(
        account={
            'balance': 100000,
            'accountType': 'type',
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901',
            'keywords': ["Exness Technologies Ltd"]
        })

    # optionally specify a provisioning profile id if servers file is not found by server name
    demo_account = await api.metatrader_account_generator_api.create_mt4_demo_account(
        account={
            'balance': 100000,
            'accountType': 'type',
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901'
        }, profile_id=provisioningProfile.id)


Create a MetaTrader 5 demo account
----------------------------------
.. code-block:: python

    demo_account = await api.metatrader_demo_account_api.create_mt5_demo_account(
        account={
            'accountType': 'type',
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'ICMarketsSC-Demo',
            'keywords': ["Raw Trading Ltd"]
        })

    # optionally specify a provisioning profile id if servers file is not found by server name
    demo_account = await api.metatrader_account_generator_api.create_mt5_demo_account(
        account={
            'accountType': 'type',
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901'
        }, profile_id=provisioningProfile.id)
