import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import CopyFactory
from metaapi_cloud_sdk.metaapi.models import format_date
from datetime import datetime
import json
import httpx

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'

# your provider MetaApi account id
# provider account must have PROVIDER value in copyFactoryRoles
provider_account_id = os.getenv('PROVIDER_ACCOUNT_ID') or '<put in your provider account id here>'

copyfactory = CopyFactory(token)


async def webhooks_example():
    api = MetaApi(token)
    try:
        configuration_api = copyfactory.configuration_api
        strategies = await configuration_api.get_strategies_with_infinite_scroll_pagination()
        strategy = next((s for s in strategies if s['accountId'] == provider_account_id), None)
        strategy_id = None
        if strategy:
            strategy_id = strategy['_id']
        else:
            strategy_id = await configuration_api.generate_strategy_id()
            strategy_id = strategy_id['id']

        print(f'Creating a strategy {strategy_id} if it does not exist')
        await configuration_api.update_strategy(strategy_id, {
            'name': 'Test strategy',
            'description': 'Some useful description about your strategy',
            'accountId': provider_account_id
        })

        print('Creating a webhook')
        webhook = await configuration_api.create_webhook(strategy_id, {
            'symbolMapping': [{'from': 'EURUSD.m', 'to': 'EURUSD'}], 'magic': 100
        })
        print('Created webhook', webhook)

        print('Updating webhook')
        await configuration_api.update_webhook(strategy_id, webhook['id'], {
            'symbolMapping': [
                {'from': 'EURUSD.m', 'to': 'EURUSD'},
                {'from': 'BTCUSD.m', 'to': 'BTCUSD'}
            ],
            'magic': 100
        })

        print('Retrieving webhooks with infinite scroll pagination')
        webhooks1 = await configuration_api.get_webhooks_with_infinite_scroll_pagination(strategy_id)
        print('Retrieved webhooks', webhooks1)

        print('Retrieving webhooks with classic pagination')
        webhooks2 = await configuration_api.get_webhooks_with_classic_scroll_pagination(strategy_id)
        print('Retrieved webhooks', webhooks2)

        print('Sending a trading signal to the webhook. Curl command:')
        payload = {
            'symbol': 'EURUSD',
            'type': 'POSITION_TYPE_BUY',
            'time': format_date(datetime.now()),
            'volume': 0.1
        }

        print(f"curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d " +
              f"'{json.dumps(payload)}' '{webhook['url']}'")
        async with httpx.AsyncClient() as client:
            response = (await client.post(webhook['url'], json=payload)).json()
            print('Sent the signal, signal ID: ' + response['signalId'])

        print('Deleting webhook ' + webhook['id'])
        await configuration_api.delete_webhook(strategy_id, webhook['id'])
    except Exception as err:
        print(api.format_error(err))

asyncio.run(webhooks_example())