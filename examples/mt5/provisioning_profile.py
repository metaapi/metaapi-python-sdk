import os
import asyncio
from metaapi_cloud_sdk import MetaApi

# Note: for information on how to use this example code please read https://metaapi.cloud/docs/client/usingCodeExamples/
# It is recommended to create accounts with automatic broker settings detection instead,
# see real_time_streaming.py

token = os.getenv('TOKEN') or '<put in your token here>'
login = os.getenv('LOGIN') or '<put in your MT login here>'
password = os.getenv('PASSWORD') or '<put in your MT password here>'
server_name = os.getenv('SERVER') or '<put in your MT server name here>'
server_dat_file = os.getenv('PATH_TO_SERVERS_DAT') or '/path/to/your/servers.dat'


async def meta_api_synchronization():
    api = MetaApi(token)
    try:
        profiles = await api.provisioning_profile_api.get_provisioning_profiles_with_infinite_scroll_pagination()

        # create test MetaTrader account profile
        profile = None
        for item in profiles:
            if item.name == server_name:
                profile = item
                break
        if not profile:
            print('Creating account profile')
            profile = await api.provisioning_profile_api.create_provisioning_profile(
                {'name': server_name, 'version': 5, 'brokerTimezone': 'EET', 'brokerDSTSwitchTimezone': 'EET'}
            )
            await profile.upload_file('servers.dat', server_dat_file)
        if profile and profile.status == 'new':
            print('Uploading servers.dat')
            await profile.upload_file('servers.dat', server_dat_file)
        else:
            print('Account profile already created')

        # Add test MetaTrader account
        accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
        account = None
        for item in accounts:
            if item.login == login and item.type.startswith('cloud'):
                account = item
                break
        if not account:
            print('Adding MT5 account to MetaApi')
            account = await api.metatrader_account_api.create_account(
                {
                    'name': 'Test account',
                    'type': 'cloud',
                    'login': login,
                    'password': password,
                    'server': server_name,
                    'provisioningProfileId': profile.id,
                    'magic': 1000,
                }
            )
        else:
            print('MT5 account already added to MetaApi')

        #  wait until account is deployed and connected to broker
        print('Deploying account')
        await account.deploy()
        print('Waiting for API server to connect to broker (may take couple of minutes)')
        await account.wait_connected()

        # connect to MetaApi API
        connection = account.get_streaming_connection()
        await connection.connect()

        # wait until terminal state synchronized to the local state
        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
        await connection.wait_synchronized({'timeoutInSeconds': 600})

        # access local copy of terminal state
        print('Testing terminal state access')
        terminal_state = connection.terminal_state
        print('connected:', terminal_state.connected)
        print('connected to broker:', terminal_state.connected_to_broker)
        print('account information:', terminal_state.account_information)
        print('positions:', terminal_state.positions)
        print('orders:', terminal_state.orders)
        print('specifications:', terminal_state.specifications)
        print('EURUSD specification:', terminal_state.specification('EURUSD'))

        # access history storage
        history_storage = connection.history_storage
        print('deals:', history_storage.deals[-5:])
        print('history orders:', history_storage.history_orders[-5:])

        await connection.subscribe_to_market_data('EURUSD')
        print('EURUSD price:', terminal_state.price('EURUSD'))

        # trade
        print('Submitting pending order')
        try:
            result = await connection.create_limit_buy_order(
                'GBPUSD', 0.07, 1.0, 0.9, 2.0, {'comment': 'comm', 'clientId': 'TE_GBPUSD_7hyINWqAlE'}
            )
            print('Trade successful, result code is ' + result['stringCode'])
        except Exception as err:
            print('Trade failed with error:')
            print(api.format_error(err))

        # finally, undeploy account after the test
        print('Undeploying MT5 account so that it does not consume any unwanted resources')
        await connection.close()
        await account.undeploy()

    except Exception as err:
        print(api.format_error(err))
    exit()


asyncio.run(meta_api_synchronization())
