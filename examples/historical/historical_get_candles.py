import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from datetime import datetime

token = os.getenv('TOKEN') or '<put in your token here>'
account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'
symbol = os.getenv('SYMBOL') or 'EURUSD'
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


async def retrieve_historical_candles():
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

        # retrieve last 10K 1m candles
        pages = 10
        print(f'Downloading {pages}K latest candles for {symbol}')
        started_at = datetime.now().timestamp()
        start_time = None
        candles = None
        for i in range(pages):
            # the API to retrieve historical market data is currently available for G1 and MT4 G2 only
            new_candles = await account.get_historical_candles(symbol, '1m', start_time)
            print(f'Downloaded {len(new_candles) if new_candles else 0} historical candles for {symbol}')
            if new_candles and len(new_candles):
                candles = new_candles
            if candles and len(candles):
                start_time = candles[0]['time']
                start_time.replace(minute=start_time.minute - 1)
                print(f'First candle time is {start_time}')
        if candles:
            print(f'First candle is', candles[0])
        print(f'Took {(datetime.now().timestamp() - started_at) * 1000}ms')

    except Exception as err:
        print(api.format_error(err))
    exit()

asyncio.run(retrieve_historical_candles())
