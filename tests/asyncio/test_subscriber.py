from pytest import mark
from pymsgbus.depends import Depends
from pymsgbus.asyncio import Subscriber

log = []
status = []

def get_log():
    return log

def get_status():
    return status

subscriber = Subscriber()

@subscriber.subscribe("train")
def sync_handler(message: str, log=Depends(get_log)):
    log.append(f"sync: {message}")

@subscriber.subscribe("train", "evaluate")
async def async_handler(message: str, status=Depends(get_status)):
    status.append(f"async: {message}")

@mark.asyncio
async def test_subscriber_receive():
    # Override dependencies for test isolation
    subscriber.override(get_log, lambda: log)
    subscriber.override(get_status, lambda: status)

    # Ensure fresh state
    log.clear()
    status.clear()

    # Simulate publisher sending messages
    await subscriber.receive("start", "train")
    await subscriber.receive("done", "evaluate")

    assert log == ["sync: start"]
    assert status == ["async: start", "async: done"]
