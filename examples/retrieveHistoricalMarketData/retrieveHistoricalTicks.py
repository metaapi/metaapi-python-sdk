import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from datetime import datetime

token = os.getenv('TOKEN') or '<put in your token here>'
account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'
symbol = os.getenv('SYMBOL') or 'EURUSD'
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


async def retrieve_historical_ticks():
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

        # retrieve last 10K ticks
        pages = 10
        print(f'Downloading {pages}K ticks for {symbol} starting from 7 days ago')
        started_at = datetime.now().timestamp()
        start_time = datetime.fromtimestamp(datetime.now().timestamp() - 7 * 24 * 60 * 60)
        offset = 0
        ticks = None
        for i in range(pages):
            # the API to retrieve historical market data is currently available for G1 and MT4 G2 only
            # historical ticks can be retrieved from MT5 only
            ticks = await account.get_historical_ticks(symbol, start_time, offset)
            print(f'Downloaded {len(ticks) if ticks else 0} historical ticks for {symbol}')
            if ticks and len(ticks):
                start_time = ticks[-1]['time']
                offset = 0
                while offset < len(ticks) and ticks[-1 - offset]['time'].timestamp() == start_time.timestamp():
                    offset += 1
                print(f'Last tick time is {start_time}, offset is {offset}')
        if ticks:
            print('Last tick is', ticks[-1])
        print(f'Took {(datetime.now().timestamp() - started_at) * 1000}ms')

    except Exception as err:
        print(api.format_error(err))
    exit()

asyncio.run(retrieve_historical_ticks())
