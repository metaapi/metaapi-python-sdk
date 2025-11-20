Debugging
==========

Socket
-------

Users can enable socket debugging to log socket interactions. The logger will record connection/disconnection events,
pings, and packets exchanged with the server.

.. code-block:: python

    from metaapi_cloud_sdk import MetaApi

    class MetaApi(token, {
        'enableSocketioDebugger': True,     # enables the socket debug logs
        'websocketLogPath': './logs.log'    # specifies the file path to save logs to
    }):
