from pymsgbus import Depends, Consumer, Producer, event
from dataclasses import dataclass

# Define a simple event
@event
class OrderPlaced:
    id: int
    item: str

# Setup test state
log = []

# Dependencies
def get_log():
    return log

# Setup Consumer and Producer
consumer = Consumer()
producer = Producer()
producer.register(consumer)

# Handlers
@consumer.handler
def on_order_placed(event: OrderPlaced, log=Depends(get_log)):
    log.append(f"Order {event.id} for {event.item}")

def test_producer_to_consumer():
    # Override dependency
    consumer.override(get_log, lambda: log)

    # Dispatch an event
    producer.dispatch(OrderPlaced(1, "Book"))

    # Assertion
    assert log == ["Order 1 for Book"]