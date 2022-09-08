# ToyRedis
Build your own Redis Implementation.

Currently supported:
* Multi-connection server utilizing event loop async code execution instead of multi threading
* Redis protocol for all the TCP messages.
* PING command to assert the server is up an running. (The server will respond with PONG).
* SET command to set a value to a key within memory storage.
* GET command to get a value from a key within memory storage.
* SET with Expiry command to set a value to a key for a specific amount of milliseconds.

Feedback is encouraged! This is simply an Python exercise and is simply a toy implementation.
