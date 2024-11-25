import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import CopyFactory

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your provider MetaApi account id
# provider account must have PROVIDER value in copyFactoryRoles
provider_account_id = os.getenv('PROVIDER_ACCOUNT_ID') or '<put in your providerAccountId here>'
# your subscriber MetaApi account id
# subscriber account must have SUBSCRIBER value in copyFactoryRoles
subscriber_account_id = os.getenv('SUBSCRIBER_ACCOUNT_ID') or '<put in your subscriberAccountId here>'


async def configure_copyfactory():
    api = MetaApi(token)
    copy_factory = CopyFactory(token)

    try:
        provider_metaapi_account = await api.metatrader_account_api.get_account(provider_account_id)
        if (
            (provider_metaapi_account is None)
            or provider_metaapi_account.copy_factory_roles is None
            or 'PROVIDER' not in provider_metaapi_account.copy_factory_roles
        ):
            raise Exception(
                'Please specify PROVIDER copyFactoryRoles value in your MetaApi '
                'account in order to use it in CopyFactory API'
            )

        subscriber_metaapi_account = await api.metatrader_account_api.get_account(subscriber_account_id)
        if (
            (subscriber_metaapi_account is None)
            or subscriber_metaapi_account.copy_factory_roles is None
            or 'SUBSCRIBER' not in subscriber_metaapi_account.copy_factory_roles
        ):
            raise Exception(
                'Please specify SUBSCRIBER copyFactoryRoles value in your MetaApi '
                'account in order to use it in CopyFactory API'
            )

        configuration_api = copy_factory.configuration_api
        strategies = await configuration_api.get_strategies_with_infinite_scroll_pagination()
        strategy = next((s for s in strategies if s['accountId'] == provider_metaapi_account.id), None)
        if strategy:
            strategy_id = strategy['_id']
        else:
            strategy_id = await configuration_api.generate_strategy_id()
            strategy_id = strategy_id['id']

        # create a strategy being copied
        await configuration_api.update_strategy(
            strategy_id,
            {
                'name': 'Test strategy',
                'description': 'Some useful description about your strategy',
                'accountId': provider_metaapi_account.id,
            },
        )

        # create subscriber
        await configuration_api.update_subscriber(
            subscriber_metaapi_account.id,
            {'name': 'Test subscriber', 'subscriptions': [{'strategyId': strategy_id, 'multiplier': 1}]},
        )
    except Exception as err:
        print(api.format_error(err))


asyncio.run(configure_copyfactory())
