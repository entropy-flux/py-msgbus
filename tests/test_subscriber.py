from pymsgbus import Depends
from pymsgbus import Subscriber
 
received_metrics = []
received_alerts = []

def get_metrics_store():
    return received_metrics

def get_alert_store():
    return received_alerts

subscriber = Subscriber()

@subscriber.subscribe("metric", "alert")
def handle_message(msg: str, store: list = Depends(get_metrics_store)):
    store.append(f"metric: {msg}")

@subscriber.subscribe("alert")
def handle_alert(msg: str, store: list = Depends(get_alert_store)):
    store.append(f"alert: {msg}")

def test_subscriber(): 
    subscriber.override(get_metrics_store, lambda: received_metrics)
    subscriber.override(get_alert_store, lambda: received_alerts) 
 
    subscriber.receive("CPU usage 90%", "metric")
    subscriber.receive("Disk failure detected", "alert")
 
    assert received_metrics == ["metric: CPU usage 90%", "metric: Disk failure detected"]
    assert received_alerts == ["alert: Disk failure detected"]
