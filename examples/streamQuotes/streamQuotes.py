import os
import asyncio
from datetime import datetime
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk.clients.metaApi.synchronizationListener import SynchronizationListener
from metaapi_cloud_sdk.metaApi.models import MetatraderSymbolPrice, MetatraderCandle, MetatraderTick, MetatraderBook, \
    MarketDataSubscription, MarketDataUnsubscription
from typing import List

token = os.getenv('TOKEN') or '<put in your token here>'
account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'
symbol = os.getenv('SYMBOL') or 'EURUSD'
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


class QuoteListener(SynchronizationListener):
    async def on_symbol_price_updated(self, instance_index: int, price: MetatraderSymbolPrice):
        if price['symbol'] == symbol:
            print(symbol + ' price updated', price)

    async def on_candles_updated(self, instance_index: int, candles: List[MetatraderCandle], equity: float = None,
                                 margin: float = None, free_margin: float = None, margin_level: float = None,
                                 account_currency_exchange_rate: float = None):
        for candle in candles:
            if candle['symbol'] == symbol:
                print(symbol + ' candle updated', candle)

    async def on_ticks_updated(self, instance_index: int, ticks: List[MetatraderTick], equity: float = None,
                               margin: float = None, free_margin: float = None, margin_level: float = None,
                               account_currency_exchange_rate: float = None):
        for tick in ticks:
            if tick['symbol'] == symbol:
                print(symbol + ' tick updated', tick)

    async def on_books_updated(self, instance_index: int, books: List[MetatraderBook], equity: float = None,
                               margin: float = None, free_margin: float = None, margin_level: float = None,
                               account_currency_exchange_rate: float = None):
        for book in books:
            if book['symbol'] == symbol:
                print(symbol + ' order book updated', book)

    async def on_subscription_downgraded(self, instance_index: int, symbol: str,
                                         updates: List[MarketDataSubscription] or None = None,
                                         unsubscriptions: List[MarketDataUnsubscription] or None = None):
        print('Market data subscriptions for ' + symbol + ' were downgraded by the server due to rate limits')


async def stream_quotes():
    api = MetaApi(token, {'domain': domain})
    try:
        account = await api.metatrader_account_api.get_account(account_id)

        #  wait until account is deployed and connected to broker
        print('Deploying account')
        if account.state != 'DEPLOYED':
            await account.deploy()
        else:
            print('Account already deployed')
        print('Waiting for API server to connect to broker (may take couple of minutes)')
        if account.connection_status != 'CONNECTED':
            await account.wait_connected()

        # create connection
        connection = account.get_streaming_connection()

        # add listener
        quote_listener = QuoteListener()
        connection.add_synchronization_listener(quote_listener)

        # connect to MetaApi API
        await connection.connect()

        # wait until terminal state synchronized to the local state
        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size), the price streaming will start once synchronization finishes')
        await connection.wait_synchronized()

        # Add symbol to MarketWatch if not yet added and subscribe to market data
        # Please note that currently only G1 and MT4 G2 instances support extended subscription management
        # Other instances will only stream quotes in response
        # Market depth streaming is available in MT5 only
        # Ticks streaming is not available for MT4 G1
        await connection.subscribe_to_market_data(symbol, [
            {'type': 'quotes', 'intervalInMilliseconds': 5000},
            {'type': 'candles', 'timeframe': '1m', 'intervalInMilliseconds': 10000},
            {'type': 'ticks'},
            {'type': 'marketDepth', 'intervalInMilliseconds': 5000}
        ])
        print('Price after subscribe:', connection.terminal_state.price(symbol))

        print(f'[{datetime.now().isoformat()}] Synchronized successfully, streaming ' + symbol + ' market data now...')

        while True:
            await asyncio.sleep(1)

    except Exception as err:
        print(api.format_error(err))

asyncio.run(stream_quotes())
