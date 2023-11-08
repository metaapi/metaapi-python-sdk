Tracking latencies
==================
You can track latencies using MetaApi.latency_monitor API. Client-side latencies include network communication delays, thus the lowest client-side latencies are achieved if you host your app in AWS Ohio region.

.. code-block:: python

    api = MetaApi('token', {'enableLatencyMonitor': True})
    monitor = api.latency_monitor
    # retrieve trade latency stats
    print(monitor.trade_latencies)
    # retrieve update streaming latency stats
    print(monitor.update_latencies)
    # retrieve quote streaming latency stats
    print(monitor.price_latencies)
    # retrieve request latency stats
    print(monitor.request_latencies)
