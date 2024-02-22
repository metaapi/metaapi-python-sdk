Access MetaTrader account via RPC API
=====================================
RPC API let you query the trading terminal state. You should use
RPC API if you develop trading monitoring apps like myfxbook or other
simple trading apps.

Query account information, positions, orders and history via RPC API
--------------------------------------------------------------------
.. code-block:: python

    connection = account.get_rpc_connection()

    await connection.connect()
    await connection.wait_synchronized()

    # retrieve balance and equity
    print(await connection.get_account_information())
    # retrieve open positions
    print(await connection.get_positions())
    # retrieve a position by id
    print(await connection.get_position(position_id='1234567'))
    # retrieve pending orders
    print(await connection.get_orders())
    # retrieve a pending order by id
    print(await connection.get_order(order_id='1234567'))
    # retrieve history orders by ticket
    print(await connection.get_history_orders_by_ticket(ticket='1234567'))
    # retrieve history orders by position id
    print(await connection.get_history_orders_by_position(position_id='1234567'))
    # retrieve history orders by time range
    print(await connection.get_history_orders_by_time_range(start_time=start_time, end_time=end_time))
    # retrieve history deals by ticket
    print(await connection.get_deals_by_ticket(ticket='1234567'))
    # retrieve history deals by position id
    print(await connection.get_deals_by_position(position_id='1234567'))
    # retrieve history deals by time range
    print(await connection.get_deals_by_time_range(start_time=start_time, end_time=end_time))

Query contract specifications and quotes via RPC API
----------------------------------------------------
.. code-block:: python

    connection = account.get_rpc_connection()

    await connection.connect()
    await connection.wait_synchronized()

    # read symbols available
    print(await connection.get_symbols())
    # read contract specification
    print(await connection.get_symbol_specification(symbol='GBPUSD'))
    # read current price
    print(await connection.get_symbol_price(symbol='GBPUSD'))

Query historical market data via RPC API
----------------------------------------
Currently this API is supported on G1 only.

.. code-block:: python

    from datetime import datetime

    # retrieve 1000 candles before the specified time
    candles = await account.get_historical_candles(symbol='EURUSD', timeframe='1m',
                                                   start_time=datetime.fromisoformat('2021-05-01'), limit=1000)

    # retrieve 1000 ticks after the specified time
    ticks = await account.get_historical_ticks(symbol='EURUSD', start_time=datetime.fromisoformat('2021-05-01'),
                                               offset=5, limit=1000)

    # retrieve 1000 latest ticks
    ticks = await account.get_historical_ticks(symbol='EURUSD', start_time=None, offset=0, limit=1000)

Execute trades
--------------
.. code-block:: python

    connection = account.get_rpc_connection()

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
            'threshold': {
                'thresholds': [
                    {
                        'threshold': 1.3,
                        'stopLoss': 1.1
                    }
                ],
                'units': 'ABSOLUTE_PRICE',
                'stopPriceBase': 'CURRENT_PRICE'
            }
        }
    }))
