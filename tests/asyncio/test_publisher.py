import pytest
from pymsgbus import Depends
from pymsgbus.asyncio import Subscriber, Publisher

# Test state
metrics = []

# Dependency
def get_metrics():
    return metrics

# Setup
subscriber = Subscriber()
publisher = Publisher()
publisher.register(subscriber)

# Handler that appends received metrics
@subscriber.subscribe("metrics")
def handle_metric(value: float, metrics=Depends(get_metrics)):
    metrics.append(value)

@pytest.mark.asyncio
async def test_publisher_to_subscriber():
    # Override the dependency
    subscriber.override(get_metrics, lambda: metrics)

    # Publish two messages
    await publisher.publish(0.95, topic="metrics")
    await publisher.publish(0.87, topic="metrics")

    # Assertions
    assert metrics == [0.95, 0.87]
