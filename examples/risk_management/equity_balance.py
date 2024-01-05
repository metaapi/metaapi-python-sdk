from metaapi_cloud_sdk import RiskManagement, EquityBalanceListener
import os
import asyncio

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your MetaApi account id
# the account must have field riskManagementApiEnabled set to true
account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


class ExampleEquityBalanceListener(EquityBalanceListener):
    async def on_equity_or_balance_updated(self, equity_balance_data):
        print('equity balance update received', equity_balance_data)

    async def on_connected(self):
        print('on connected event received')

    async def on_disconnected(self):
        print('on disconnected event received')

    async def on_error(self, error: Exception):
        print('error event received', error)


async def main():
    try:
        risk_management = RiskManagement(token, {'domain': domain})
        risk_management_api = risk_management.risk_management_api

        # adding an equity balance listener
        equity_balance_listener = ExampleEquityBalanceListener(account_id)
        listener_id = await risk_management_api.add_equity_balance_listener(equity_balance_listener, account_id)

        print('Streaming equity balance for 1 minute...')
        await asyncio.sleep(60)
        risk_management_api.remove_equity_balance_listener(listener_id)
        print('Listener removed')
    except Exception as err:
        print(RiskManagement.format_error(err))
    exit()


asyncio.run(main())
