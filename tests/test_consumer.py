from pymsgbus import Depends
from pymsgbus import event
from pymsgbus import Consumer 
from dataclasses import dataclass
 
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

def getdb() -> dict: 
    ...

def getnfs() -> list: 
    ...

def register(name: str):
    user = User(1, name)
    consumer.consume(Created(user))

def update(id: int, name: str):
    user = User(id, name)
    consumer.consume(Updated(user))

@consumer.handler
def handle_put(event: Created[User] | Updated[User], db: dict = Depends(getdb)):
    db[event.entity.id] = event.entity.name

@consumer.handler
def handle_registered(event: Created[User]):
    consumer.consume(RegistrationDone(f"User {event.entity.id} registered."))

@consumer.handler
def handle_registered(event: RegistrationDone, nfs: list = Depends(getnfs)):
    nfs.append(event.text)

db = {}
nfs = []

def test_consumer(): 
    consumer.override(getdb, lambda: db)
    consumer.override(getnfs, lambda: nfs)

    register('test')
    update(1, 'updated')

    assert db[1] == 'updated'
    assert nfs == ["User 1 registered."]