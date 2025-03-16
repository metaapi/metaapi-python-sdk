MetaApi risk management API for Python (a member of `metaapi.cloud <https://metaapi.cloud>`_ project)
#####################################################################################################

MetaApi risk management API is a cloud API for executing trading challenges and competitions. You can use this API for
e.g. if you want to launch a proprietary trading company like FTMO. The API is also useful for trading firms/teams
which have to enforce trading risk restrictions.

MetaApi risk management API is a member of MetaApi project (`https://metaapi.cloud <https://metaapi.cloud>`_),
a powerful cloud forex trading API which supports both MetaTrader 4 and MetaTrader 5 platforms.

MetaApi is a paid service, however we may offer a free tier access in some cases.

The `MetaApi pricing <https://metaapi.cloud/#pricing>`_ was developed with the intent to make your charges less or equal
to what you would have to pay for hosting your own infrastructure. This is possible because over time we managed to heavily
optimize our MetaTrader infrastructure. And with MetaApi you can save significantly on application development and
maintenance costs and time thanks to high-quality API, open-source SDKs and convenience of a cloud service.

This SDK requires a 3.8+ version of Python to run.

Why do we offer MetaApi risk management API
===========================================

We found that developing a platform and infrastructure for running trading and investement challenges and competitions
is a task which requires lots of effort and investment.

We decided to share our product as it allows developers to start with a powerful solution in almost no time, saving on
development and infrastructure maintenance costs.

MetaApi risk management API features
=====================================

Features supported:

- fine-granular equity tracking
- configuring and executing trading challenges and competitions consisting from multiple drawdown and profit target criteria
- receiving notifications about failed challenges in real time
- tracking equity chart and challenge/competition statistics in real time
- tracking equity and balance changes in real time
- tracking number of days with trades during a challenge

Please check Features section of the `https://metaapi.cloud/docs/risk-management/ <https://metaapi.cloud/docs/risk-management/>`_
documentation for detailed description of all settings you can make.

REST API documentation
======================

RiskManagement SDK is built on top of RiskManagement REST API.

RiskManagement REST API docs are available at `https://metaapi.cloud/docs/risk-management/ <https://metaapi.cloud/docs/risk-management/>`_

FAQ
===

Please check this page for FAQ: `https://metaapi.cloud/docs/risk-management/faq/ <https://metaapi.cloud/docs/risk-management/faq/>`_.

Code examples
=============

Please check examples folder for code examples.

Configuring equity tracking
===========================

In order to configure equity tracking you need to:

- add MetaApi MetaTrader accounts with `riskManagementApiEnabled` field set to true (see below)
- create equity trackers for the accounts with needed parameters

.. code-block:: python

    from metaapi_cloud_sdk import MetaApi, RiskManagement

    token = '...'
    metaapi = MetaApi(token=token)
    risk_management = RiskManagement(token=token)

    # retrieve MetaApi MetaTrader accounts with riskManagementApiEnabled field set to true
    account = await api.metatrader_account_api.get_account(account_id='accountId')
    if not account.risk_management_api_enabled:
        raise Exception('Please set riskManagementApiEnabled field to true in your MetaApi account in ' +
            'order to use it in RiskManagement API')

    risk_management_api = risk_management.risk_management_api

    # create a tracker
    tracker_id = await risk_management_api.create_tracker('accountId', {
        'name': 'Test tracker',
        'period': 'day',
        'absoluteDrawdownThreshold': 100
    })

    # retrieve list of trackers
    print(await risk_management_api.get_trackers('accountId'))

    # retrieve a tracker by id
    print(await risk_management_api.get_tracker('accountId', 'trackerId'))

    # update a tracker
    print(await risk_management_api.update_tracker('accountId', tracker_id['id'], {'name': 'Updated name'}))

    # remove a tracker
    print(await risk_management_api.delete_tracker('accountId', tracker_id['id']))

See in-code documentation for full definition of possible configuration options.

Retrieving equity tracking events and statistics
================================================

RiskManagement allows you to monitor equity profits and drawdowns on trading accounts.

Retrieving tracker events
--------------------------
.. code-block:: python

    # retrieve tracker events, please note that this method supports filtering by broker time range, accountId, trackerId
    # and limits number of records
    print(await risk_management_api.get_tracker_events('2022-04-13 09:30:00.000', '2022-05-14 09:30:00.000'))

Streaming tracker events
-------------------------

You can subscribe to a stream of tracker events using the tracker event listener.

.. code-block:: python

    from metaapi_cloud_sdk import TrackerEventListener

    # create a custom class based on the TrackerEventListener
    class Listener(TrackerEventListener):

        # specify the function called on events arrival
        async def on_tracker_event(tracker_event):
            print('Tracker event', tracker_event)

    # add listener
    listener = Listener('accountId', 'trackerId1')
    listener_id = risk_management_api.add_tracker_event_listener(listener)

    # remove listener
    risk_management_api.remove_tracker_event_listener(listener_id)

Retrieving tracking statistics
------------------------------
.. code-block:: python

    # retrieve tracking statistics, please note that this method can filter returned data and supports pagination
    print(await risk_management_api.get_tracking_statistics('accountId', tracker_id['id']))

Streaming period statistics events
----------------------------------

You can subscribe to a stream of period statistics events using the period statistics event listener.

.. code-block:: python

    from metaapi_cloud_sdk import PeriodStatisticsListener

    # create a custom class based on the PeriodStatisticsListener
    class Listener(PeriodStatisticsListener):

        # specify the function called on events arrival
        async def on_period_statistics_updated(self, period_statistics_event):
            print('Period statistics updated', period_statistics_event)

        # specify the function called on period complete
        async def on_period_statistics_completed(self):
            print('Period statistics period completed')

        # specify the function called on tracker period complete
        async def on_tracker_completed(self):
            print('Tracker period completed')

        # specify the function called on connection established
        async def on_connected(self):
            print('Connection established')

        # specify the function called on connection lost
        async def on_disconnected(self):
            print('Connection lost')

    # add listener
    listener = Listener('accountId', 'trackerId1')
    listener_id = await risk_management_api.add_period_statistics_listener(listener, 'accountId', 'trackerId1')

    # remove listener
    risk_management_api.remove_period_statistics_listener(listener_id)

Retrieving equity chart
-----------------------
.. code-block:: python

    # retrieve equity chart, please note that this method supports loading within specified broker time
    print(await risk_management_api.get_equity_chart('accountId'))

Streaming equity chart events
-----------------------------
.. code-block:: python

    from metaapi_cloud_sdk import EquityChartListener

    # create a custom class based on the EquityChartListener
    class Listener(EquityChartListener):

        # specify the function called on events arrival
        async def on_equity_record_updated(self, equity_chart_event):
            print('Equity chart updated', equity_chart_event)

        # specify the function called on period complete
        async def on_equity_record_completed(self):
            print('Equity chart period completed')

        # specify the function called on connection established
        async def on_connected(self):
            print('Connection established')

        # specify the function called on connection lost
        async def on_disconnected(self):
            print('Connection lost')

    # add listener
    listener = Listener('accountId')
    listener_id = await risk_management_api.add_equity_chart_listener(listener, 'accountId')

    # remove listener
    risk_management_api.remove_equity_chart_listener(listener_id)

Equity/balance tracking
-----------------------

You can subscribe to a stream of equity/balance events using the equity balance event listener.

.. code-block:: python

    from metaapi_cloud_sdk import EquityBalanceListener

    # create a custom class based on the EquityBalanceListener
    class Listener(EquityBalanceListener):

        # specify the function called on events arrival
        async def on_equity_or_balance_updated(self, equity_balance_data):
            print('Equity/balance updated', equity_balance_data)

        # specify the function called on connection established
        async def on_connected(self):
            print('Connection established')

        # specify the function called on connection lost
        async def on_disconnected(self):
            print('Connection lost')

    # add listener
    listener = Listener('accountId')
    listener_id = await risk_management_api.add_equity_balance_listener(listener, 'accountId')

    # remove listener
    risk_management_api.remove_equity_balance_listener(listener_id)
