from pymsgbus import Depends, Subscriber, Publisher
 
metrics = []
 
def get_metrics():
    return metrics
 
subscriber = Subscriber()
publisher = Publisher()
publisher.register(subscriber)
 
@subscriber.subscribe("metrics")
def handle_metric(value: float, metrics=Depends(get_metrics)):
    metrics.append(value)

def test_publisher_to_subscriber(): 
    subscriber.override(get_metrics, lambda: metrics)
 
    publisher.publish(0.95, topic="metrics")
    publisher.publish(0.87, topic="metrics")
 
    assert metrics == [0.95, 0.87]