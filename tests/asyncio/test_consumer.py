import pytest
from dataclasses import dataclass
from pymsgbus import Depends, event
from pymsgbus.asyncio import Consumer  

@event
class Created[T]:
    entity: T

@event
class Updated[T]:
    entity: T

@dataclass
class User:
    id: int
    name: str

@event
class RegistrationDone:
    text: str

consumer = Consumer()

def getdb():
    return db

async def getnfs(): 
    yield nfs


@consumer.handler
def handle_put(event: Created[User] | Updated[User], db: dict = Depends(getdb)):
    db[event.entity.id] = event.entity.name

@consumer.handler
async def handle_registered(event: Created[User]):
    await consumer.consume(RegistrationDone(f"User {event.entity.id} registered."))

@consumer.handler
def handle_registered_done(event: RegistrationDone, nfs: list = Depends(getnfs)):
    nfs.append(event.text)
 
db = {}
nfs = []

@pytest.mark.asyncio
async def test_consumer(): 
    consumer.override(getdb, lambda: db)
    consumer.override(getnfs, lambda: nfs)
 
    await consumer.consume(Created(User(1, 'test')))
    await consumer.consume(Updated(User(1, 'updated')))
 
    assert db[1] == 'updated'
    assert nfs == ["User 1 registered."]
