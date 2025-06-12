from pytest import mark 
from pymsgbus import Depends, event
from pymsgbus.asyncio import Consumer, Producer  
 
@event
class OrderPlaced:
    id: int
    item: str
 
log = []
 
async def get_log():
    return log
 
consumer = Consumer()
producer = Producer()
producer.register(consumer)

# Handler
@consumer.handler
async def on_order_placed(event: OrderPlaced, log=Depends(get_log)):
    log.append(f"Order {event.id} for {event.item}")

@mark.asyncio
async def test_producer_to_consumer(): 
    consumer.override(get_log, lambda: log)
 
    await producer.dispatch(OrderPlaced(1, "Book"))
 
    assert log == ["Order 1 for Book"]
