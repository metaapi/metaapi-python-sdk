import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import CopyFactory, UserLogListener


# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'

# your subscriber id
subscriber_id = os.getenv('SUBSCRIBER_ID') or '<put in your subscriber id here>'

copyfactory = CopyFactory(token)


class Listener(UserLogListener):
    async def on_user_log(self, log_event):
        print('Log event', log_event)

    async def on_error(self, error: Exception):
        print('Error event', error)


async def user_log_listener_example():
    api = MetaApi(token)
    try:
        listener = Listener()

        trading_api = copyfactory.trading_api
        listener_id = trading_api.add_subscriber_log_listener(listener, subscriber_id)

        while True:
            await asyncio.sleep(10)

        trading_api.remove_subscriber_log_listener(listener_id)
    except Exception as err:
        print(api.format_error(err))

asyncio.run(user_log_listener_example())
