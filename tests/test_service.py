from pymsgbus import Depends, Service

log = []
config = {"device": "cpu"}

def get_log():
    return log

def get_config():
    return config

service = Service()

@service.handler
def train_model(epochs: int, log=Depends(get_log), config=Depends(get_config)):
    msg = f"Training on {config['device']} for {epochs} epochs"
    log.append(msg)
    return msg

@service.handler
def reset_log(log=Depends(get_log)):
    log.clear()
    return "log reset"

def test_service():
    service.override(get_log, lambda: log)
    service.override(get_config, lambda: {"device": "cuda"})

    result1 = service.execute("train-model", 5)
    result2 = service.execute("reset-log")

    assert result1 == "Training on cuda for 5 epochs"
    assert result2 == "log reset"
    assert log == []  # log was cleared