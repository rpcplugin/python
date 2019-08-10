# rpcplugin for Python

This is a Python library implementing the [rpcplugin](https://www.rpcplugin.org/)
protocol, allowing an application written in Python to consume plugins as
a client, or allowing plugin servers to be written in Python.

The rpcplugin protocol is a low-level protocol built around
[gRPC](https://www.grpc.io/). If you're intending to write a plugin for an
application that uses this protocol, check first to see if that application
offers an application-specific Python SDK that wraps this library, so you
can avoid dealing with low-level gRPC details and Protocol Buffers definitions.
