from metaapi_cloud_sdk import RiskManagement, TrackerEventListener
import os
import asyncio
import json

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your MetaApi account id
# the account must have field riskManagementApiEnabled set to true
account_id = os.getenv('ACCOUNT_ID') or '<put in your account id here>'
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


class ExampleTrackerEventListener(TrackerEventListener):
    async def on_tracker_event(self, tracker_event):
        print('tracker event received', json.dumps(tracker_event))

    async def on_error(self, error: Exception):
        print('error event received', error)


async def main():
    try:
        risk_management = RiskManagement(token, {'domain': domain})
        risk_management_api = risk_management.risk_management_api

        # creating a tracker
        tracker_id = await risk_management_api.create_tracker(
            account_id, {'name': 'example-tracker-3', 'absoluteDrawdownThreshold': 5, 'period': 'day'}
        )
        print('Created an event tracker ' + tracker_id['id'])

        # adding a tracker event listener
        tracker_event_listener = ExampleTrackerEventListener(account_id, tracker_id['id'])
        listener_id = risk_management_api.add_tracker_event_listener(
            tracker_event_listener, account_id, tracker_id['id']
        )

        print('Streaming tracking events for 1 minute...')
        await asyncio.sleep(60)
        risk_management_api.remove_tracker_event_listener(listener_id)

        print('Receiving statistics with REST API')
        events = await risk_management_api.get_tracker_events(None, None, account_id, tracker_id['id'])
        print('tracking events', json.dumps(events))
        statistics = await risk_management_api.get_tracking_statistics(account_id, tracker_id['id'])
        print('tracking statistics', json.dumps(statistics))
        equity_chart = await risk_management_api.get_equity_chart(account_id)
        print('equity chart', json.dumps(equity_chart))

        # removing the tracker
        await risk_management_api.delete_tracker(account_id, tracker_id['id'])
        print('Removed the tracker')
    except Exception as err:
        print(RiskManagement.format_error(err))
    exit()


asyncio.run(main())
