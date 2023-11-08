Enable Logging logging
===========================================
By default SDK logs messages to console. You can select the SDK to use `logging <https://docs.python.org/3/library/logging.html>`_ logging
library by calling `MetaApi.enable_logging()` static method before creating MetaApi instances.
.. code-block:: python

    from metaapi_cloud_sdk import MetaApi

    MetaApi.enable_logging()

    meta_api = MetaApi(token)

Please note that the SDK does not configure logging automatically. If you decide to use logging, then your application
is still responsible to configuring logging appenders and categories. Please refer to logging documentation for details.
