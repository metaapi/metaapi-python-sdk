from metaapi_cloud_sdk import RiskManagement, EquityChartListener
import os
import asyncio
import json

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your MetaApi account id
# the account must have field riskManagementApiEnabled set to true
account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


class ExampleEquityChartListener(EquityChartListener):
    async def on_equity_record_updated(self, equity_chart_event):
        print('equity record updated event received', equity_chart_event)

    async def on_equity_record_completed(self):
        print('equity record completed event received')

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

        # adding an equity chart listener
        equity_chart_listener = ExampleEquityChartListener(account_id)
        listener_id = await risk_management_api.add_equity_chart_listener(equity_chart_listener, account_id)

        print('Streaming equity chart events for 1 minute...')
        await asyncio.sleep(60)
        risk_management_api.remove_equity_chart_listener(listener_id)

        equity_chart = await risk_management_api.get_equity_chart(account_id)
        print('equity chart', json.dumps(equity_chart))
    except Exception as err:
        print(RiskManagement.format_error(err))
    exit()


asyncio.run(main())
