from metaapi_cloud_sdk import MetaStats, MetaApi
import asyncio
import os


async def example_request():
    # your MetaApi API token
    token = os.getenv('TOKEN') or '<put in your token here>'
    # your MetaApi account id
    account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'

    api = MetaApi(token)
    meta_stats = MetaStats(token)
    # you can configure http client via second parameter,
    # see in-code documentation for full definition of possible configuration options

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

        metrics = await meta_stats.get_metrics(account_id)
        print(metrics)  # -> {'trades': ..., 'balance': ..., ...}

        trades = await meta_stats.get_account_trades(account_id, '0000-01-01 00:00:00.000', '9999-01-01 00:00:00.000')
        print(trades[-5:])  # -> {_id: ..., gain: ..., ...}

        open_trades = await meta_stats.get_account_open_trades(account_id)
        print(open_trades)  # -> {_id: ..., gain: ..., ...}

    except Exception as err:
        print(meta_stats.format_error(err))
    exit(0)

asyncio.run(example_request())
