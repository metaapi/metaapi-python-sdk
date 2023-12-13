metaapi.cloud SDK for Python
############################

MetaApi is a powerful, fast, cost-efficient, easy to use and standards-driven cloud forex trading API for MetaTrader 4 and MetaTrader 5 platform designed for traders, investors and forex application developers to boost forex application development process. MetaApi can be used with any broker and does not require you to be a brokerage.

CopyFactory is a simple yet powerful copy-trading API which is a part of MetaApi. See below for CopyFactory readme section.

MetaApi is a paid service, however we offer a free tier for testing and personal use.

The `MetaApi pricing <https://metaapi.cloud/#pricing>`_ was developed with the intent to make your charges less or equal to what you would have to pay
for hosting your own infrastructure. This is possible because over time we managed to heavily optimize
our MetaTrader infrastructure. And with MetaApi you can save significantly on application development and
maintenance costs and time thanks to high-quality API, open-source SDKs and convenience of a cloud service.

Official REST and websocket API documentation: https://metaapi.cloud/docs/client/

This SDK requires a 3.8+ version of Python to run.

Please note that this SDK provides an abstraction over REST and websocket API to simplify your application logic.

For more information about SDK APIs please check docstring documentation in source codes located inside lib folder of this package.

Working code examples
=====================
Please check `this short video <https://youtu.be/LIqFOOOLP-g>`_ to see how you can download samples via our web application.

You can find code examples at `examples folder of our github repo <https://github.com/metaapi/metaapi-python-sdk/tree/master/examples>`_ or in the examples folder of the pip package.

We have composed a `short guide explaining how to use the example code <https://metaapi.cloud/docs/client/usingCodeExamples/>`_

Installation
============
.. code-block:: bash

    pip install metaapi-cloud-sdk

Connecting to MetaApi
=====================
Please use one of these ways:

1. https://app.metaapi.cloud/token web UI to obtain your API token.
2. An account access token which grants access to a single account. See section below on instructions on how to retrieve account access token.

Supply token to the MetaApi class constructor.

.. code-block:: python

    from metaapi_cloud_sdk import MetaApi

    token = '...'
    api = MetaApi(token=token)

Retrieving account access token
===============================
Account access token grants access to a single account. You can retrieve account access token via API:

.. code-block:: python

    account_id = '...'
    validity_in_hours = 24
    account_access_token = await api.token_management_api.narrow_down_token(
        {
            'applications': ['trading-account-management-api', 'copyfactory-api', 'metaapi-rest-api', 'metaapi-rpc-api', 'metaapi-real-time-streaming-api', 'metastats-api', 'risk-management-api'],
            'roles': ['reader'],
            'resources': [{'entity': 'account', 'id': account_id}]

        },
        validity_in_hours
    )
    print(account_access_token)

Alternatively, you can retrieve account access token via web UI on https://app.metaapi.cloud/accounts page (see `this video <https://youtu.be/PKYiDns6_xI>`_).

Table of contents
=================

1. `MT account management <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/metaApi/managingAccounts.rst>`_

2. `MetaApi RPC API <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/metaApi/rpcApi.rst>`_

3. `MetaApi real-time streaming API (websocket API) <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/metaApi/streamingApi.rst>`_

4. `Risk management API <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/riskManagement.rst>`_

5. `CopyFactory copy trading API <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/copyTrading.rst>`_

6. `MetaStats trading statistics API <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/metaStats.rst>`_

7. `MetaApi MT manager API <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/managerApi.rst>`_

8. `Tracking latencies <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/trackingLatencies.rst>`_

9. `Enable log4js logging <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/logging.rst>`_

10. `Rate limits & quotas <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/rateLimits.rst>`_

11. `Token management API <https://github.com/metaapi/metaapi-python-sdk/blob/master/docs/tokenManagementApi.rst>`_
