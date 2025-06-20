# Copyright 2025 Eric Cardozo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You can obtain a copy of the License at:
# 
#     http://www.apache.org/licenses/LICENSE-2.0
#
# This software is distributed "AS IS," without warranties or conditions.
# See the License for specific terms.  

from typing import Any
from collections.abc import Callable
from pymsgbus.depends import inject, Provider
from pymsgbus.depends import Depends as Depends
        
class Subscriber:
    """
    A **subscriber** is a component that listens for messages published by a **publisher** on
    a given **topic** processes them accordingly.

    Unlike a **consumer**, a **subscriber** receives messages only from the topics it has subscribed to
    and it's the **publisher**'s responsibility to route the messages accordingly.

    Methods: 
        override:
            Overrides a dependency with a concrete implementation.
        subscribe:
            Decorator for registering a handler function to one or more topics.
        receive:
            Receives a message from a given topic directly and triggers the corresponding 
            handler functions to process it.

    Example:
        ```python	
        subscriber = Subscriber()

        @subscriber.subscribe('metrics')
        def store_metric(metrics: list):
            for metric in metrics:
                subscriber.receive(metric, metric['name'])

        @subscriber.subscribe('loss')
        def on_loss(loss):
            print(f"Loss: {loss['value']}")

        @subscriber.subscribe('accuracy')
        def on_accuracy(accuracy):
            print(f"Accuracy: {accuracy['value']}")

        subscriber.receive([
            {'name': 'loss', 'value': 0.1}, 
            {'name': 'accuracy', 'value': 0.9}], 
        topic='metrics')

        # Output:
        # Loss: 0.1
        # Accuracy: 0.9
        ```        
    """
    def __init__(
        self, 
        provider: Provider | None = None
    ): 
        self.provider = provider or Provider()
        self.handlers = dict[str, list[Callable[..., None]]]()
    
    @property
    def dependency_overrides(self) -> dict:
        """
        Returns the dependency overrides for the subscriber. This is useful for late binding,
        testing and changing the behavior of the subscriber in runtime. 

        Returns:
            dict: A dictionary of the dependency map.
        """
        return self.provider.dependency_overrides
    
    
    def override(self, dependency: Callable, implementation: Callable):
        """
        Overrides a dependency with an implementation. 

        Args:
            dependency (Callable): The dependency function to override.
            implementation (Callable): The implementation of the function.
        """
        self.dependency_overrides[dependency] = implementation

    
    def register(self, topic: str, wrapped: Callable[..., None]) -> None:       
        """
        Registers a handler function with a given topic. Don't use this directly,
        use the `subscribe` decorator instead.

        Args:
            topic (str): The topic to register the handler function to.
            wrapped (Callable[..., None]): The handler function to register.
        """ 
        injected = inject(self.provider)(wrapped)
        self.handlers.setdefault(topic, []).append(injected)
    

    def subscribe(self, *topics: str) -> Callable[..., None]:
        """
        Decorator for registering a handler function to one or more topics. 
        Args:

            *topics (str): The topics to register the handler function to.

        Returns:
            Callable[..., None]: The decorated handler function.
        """
        def handler(wrapped: Callable[..., None]):
            for topic in topics:
                self.register(topic, wrapped)
            return wrapped
        return handler
    

    def receive(self, message: Any, topic: str):
        """
        Receives a message from a given topic and triggers the corresponding handler functions
        to process it. This is called by the **publisher** but is also useful for deliver messages
        between handlers directly.

        Args:
            message (Any): The message to process.
            topic (str): The topic to process the message from.
        """
        for handler in self.handlers.get(topic, []):
            handler(message)