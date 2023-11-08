Use real-time streaming API
---------------------------
Real-time streaming API is good for developing trading applications like trade copiers or automated trading strategies.
The API synchronizes the terminal state locally so that you can query local copy of the terminal state really fast.

Synchronizing and reading terminal state
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    from datetime import datetime

    account = await api.metatrader_account_api.get_account(account_id='accountId')
    connection = account.get_streaming_connection()
    await connection.connect()

    # access local copy of terminal state
    terminalState = connection.terminal_state

    # wait until synchronization completed
    await connection.wait_synchronized()

    print(terminalState.connected)
    print(terminalState.connected_to_broker)
    print(terminalState.account_information)
    print(terminalState.positions)
    print(terminalState.orders)
    # symbol specifications
    print(terminalState.specifications)
    print(terminalState.specification(symbol='EURUSD'))
    print(terminalState.price(symbol='EURUSD'))

    # access history storage
    historyStorage = connection.history_storage

    # both orderSynchronizationFinished and dealSynchronizationFinished
    # should be true once history synchronization have finished
    print(historyStorage.order_synchronization_finished)
    print(historyStorage.deal_synchronization_finished)

    print(historyStorage.deals)
    print(historyStorage.get_deals_by_ticket('1'))
    print(historyStorage.get_deals_by_position('1'))
    print(historyStorage.get_deals_by_time_range(
        datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), datetime.now())

    print(historyStorage.history_orders)
    print(historyStorage.get_history_orders_by_ticket('1'))
    print(historyStorage.get_history_orders_by_position('1'))
    print(historyStorage.get_history_orders_by_time_range(
        datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), datetime.now())

Overriding local history storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default history is stored in memory only. You can override history storage to save trade history to a persistent storage like MongoDB database.

.. code-block:: python

    from metaapi_cloud_sdk import HistoryStorage

    class MongodbHistoryStorage(HistoryStorage):
        # implement the abstract methods, see MemoryHistoryStorage for sample
        # implementation

    historyStorage = MongodbHistoryStorage()

    # Note: if you will not specify history storage, then in-memory storage
    # will be used (instance of MemoryHistoryStorage)
    connection = account.get_streaming_connection(history_storage=historyStorage)
    await connection.connect()

    # access history storage
    historyStorage = connection.history_storage;

    # invoke other methods provided by your history storage implementation
    print(await historyStorage.yourMethod())

Receiving synchronization events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can override SynchronizationListener in order to receive synchronization event notifications, such as account/position/order/history updates or symbol quote updates.

.. code-block:: python

    from metaapi_cloud_sdk import SynchronizationListener

    # receive synchronization event notifications
    # first, implement your listener
    class MySynchronizationListener(SynchronizationListener):
        # override abstract methods you want to receive notifications for

    # retrieving a connection
    connection = account.get_streaming_connection(history_storage=historyStorage)

    # now add the listener
    listener = MySynchronizationListener()
    connection.add_synchronization_listener(listener=listener)

    # open the connection after adding listeners
    await connection.connect()

    # remove the listener when no longer needed
    connection.remove_synchronization_listener(listener=listener)

Retrieve contract specifications and quotes via streaming API
-------------------------------------------------------------
.. code-block:: python

    connection = account.get_streaming_connection()
    await connection.connect()

    await connection.wait_synchronized()

    # first, subscribe to market data
    await connection.subscribe_to_market_data(symbol='GBPUSD')

    # read contract specification
    print(terminalState.specification(symbol='EURUSD'))

    # read current price
    print(terminalState.price(symbol='EURUSD'))

    # unsubscribe from market data when no longer needed
    await connection.unsubscribe_from_market_data(symbol='GBPUSD')

Execute trades
--------------
.. code-block:: python

    connection = account.get_streaming_connection()

    await connection.connect()
    await connection.wait_synchronized()

    # trade
    print(await connection.create_market_buy_order(symbol='GBPUSD', volume=0.07, stop_loss=0.9, take_profit=2.0,
        options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_market_sell_order(symbol='GBPUSD', volume=0.07, stop_loss=2.0, take_profit=0.9,
        options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_limit_buy_order(symbol='GBPUSD', volume=0.07, open_price=1.0, stop_loss=0.9,
        take_profit=2.0, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_limit_sell_order(symbol='GBPUSD', volume=0.07, open_price=1.5, stop_loss=2.0,
        take_profit=0.9, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_buy_order(symbol='GBPUSD', volume=0.07, open_price=1.5, stop_loss=2.0,
        take_profit=0.9, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_sell_order(symbol='GBPUSD', volume=0.07, open_price=1.0, stop_loss=2.0,
        take_profit=0.9, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_limit_buy_order(symbol='GBPUSD', volume=0.07, open_price=1.5,
        stop_limit_price=1.4, stop_loss=0.9, take_profit=2.0, options={'comment': 'comment',
        'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_limit_sell_order(symbol='GBPUSD', volume=0.07, open_price=1.0,
        stop_limit_price=1.1, stop_loss=2.0, take_profit=0.9, options={'comment': 'comment',
        'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.modify_position(position_id='46870472', stop_loss=2.0, take_profit=0.9))
    print(await connection.close_position_partially(position_id='46870472', volume=0.9))
    print(await connection.close_position(position_id='46870472'))
    print(await connection.close_by(position_id='46870472', opposite_position_id='46870482'))
    print(await connection.close_positions_by_symbol(symbol='EURUSD'))
    print(await connection.modify_order(order_id='46870472', open_price=1.0, stop_loss=2.0, take_profit=0.9))
    print(await connection.cancel_order(order_id='46870472'))

    # if you need to, check the extra result information in stringCode and numericCode properties of the response
    result = await connection.create_market_buy_order(symbol='GBPUSD', volume=0.07, stop_loss=0.9, take_profit=2.0,
        options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print('Trade successful, result code is ' + result['stringCode'])

    # catch and output exception
    try:
        await connection.create_market_buy_order(symbol='GBPUSD', volume=0.07, stop_loss=0.9, take_profit=2.0,
            options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'})
    except Exception as err:
        print(api.format_error(err))

Trailing stop loss
^^^^^^^^^^^^^^^^^^
Trailing stop loss is a trade option that allows you to automatically configure and change the order/position stop loss
based on the current price of the symbol. The specified settings are run on the server and modify the stop loss
regardless of your connection to the account. The stop loss can be modified no more often than once in 15 seconds. Two
types of trailing stop loss are available: distance stop loss and threshold stop loss, but both can be specified at the
same time. You can find the full description here:
`https://metaapi.cloud/docs/client/models/trailingStopLoss/ <https://metaapi.cloud/docs/client/models/trailingStopLoss/>`_

.. code-block:: python

    # distance trailing stop loss
    print(await connection.create_market_buy_order('GBPUSD', 0.07, 0.9, 2.0, {
        'trailingStopLoss': {
            'distance': {
                'distance': 200,
                'units': 'RELATIVE_POINTS'
            }
        }
    }))

    # threshold trailing stop loss
    print(await connection.create_market_buy_order('GBPUSD', 0.07, 0.9, 2.0, {
        'trailingStopLoss': {
            'thresholds': [
                {
                    'threshold": 50,
                    'stopLoss": 100
                },
                {
                    'threshold": 100,
                    'stopLoss": 50
                }
            ],
            'units': 'RELATIVE_POINTS'
        }
    }))

Monitoring account connection health and uptime
===============================================
You can monitor account connection health using MetaApiConnection.health_monitor API.

.. code-block:: python

    monitor = connection.health_monitor
    # retrieve server-side app health status
    print(monitor.server_health_status)
    # retrieve detailed connection health status
    print(monitor.health_status)
    # retrieve account connection update measured over last 7 days
    print(monitor.uptime)
