import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import CopyFactory, StopoutListener

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'


async def stopout_example():
    api = MetaApi(token)
    copy_factory = CopyFactory(token)

    class Listener(StopoutListener):
        async def on_stopout(self, strategy_stopout_event):
            print('Strategy stopout event', strategy_stopout_event)

        async def on_error(self, error: Exception):
            print('Error event', error)

    try:
        listener = Listener()

        trading_api = copy_factory.trading_api
        listener_id = trading_api.add_stopout_listener(listener)

        while True:
            await asyncio.sleep(10)

        trading_api.remove_stopout_listener(listener_id)
    except Exception as err:
        print(api.format_error(err))

asyncio.run(stopout_example())
