from metaapi_cloud_sdk import RiskManagement, PeriodStatisticsListener
import os
import asyncio
import json

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your MetaApi account id
# the account must have field riskManagementApiEnabled set to true
account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


class ExamplePeriodStatisticsListener(PeriodStatisticsListener):
    async def on_period_statistics_updated(self, period_statistics_event):
        print('period statistics updated', period_statistics_event)

    async def on_period_statistics_completed(self):
        print('period completed event received')

    async def on_tracker_completed(self):
        print('tracker completed event received')

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

        # creating a tracker
        tracker_id = await risk_management_api.create_tracker(
            account_id, {'name': 'example-tracker-5', 'absoluteDrawdownThreshold': 5, 'period': 'day'}
        )
        print('Created an event tracker ' + tracker_id['id'])

        # adding a period statistics listener
        period_statistics_listener = ExamplePeriodStatisticsListener(account_id, tracker_id['id'])
        listener_id = await risk_management_api.add_period_statistics_listener(
            period_statistics_listener, account_id, tracker_id['id']
        )

        print('Streaming period statistics events for 1 minute...')
        await asyncio.sleep(60)
        risk_management_api.remove_period_statistics_listener(listener_id)

        equity_chart = await risk_management_api.get_equity_chart(account_id)
        print('equity chart', json.dumps(equity_chart))
    except Exception as err:
        print(RiskManagement.format_error(err))
    exit()


asyncio.run(main())
