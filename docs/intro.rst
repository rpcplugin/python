Getting Started
===============

The ``example`` directory of the ``rpcplugin`` Python implementation repository
contains example plugin client (host application) and server (the plugins
themselves) implementations for a simple RPC service that just counts calls
and returns how many times it has been called.

From within that directory, running ``python client.py`` will initialize a
plugin client, launch the server implementation in ``server.py``, and then call
it in a loop to illustrate the counting behavior. In this case both the client
and server are written in Python, but that is not a requirement: the server
could've been written in any language with an RPCPlugin_ implementation.

In the remainder of this section, we'll look at how that example is put
together, and thus show how you might use ``rpcplugin`` to write your own
plugins for RPCPlugin-based applications or integrate plugins into your
application.

gRPC and Protocol Buffers
-------------------------

In order to communicate with plugins written in various languages, RPCPlugin
uses the languge-agnostic RPC framework gRPC_, with the plugin RPC protocol
defined using `Protocol Buffers`_.

For our counting example, the service is defined in ``countplugin1.proto``.
In that file we can find the language-agnostic definition of the count
service using the Protocol Buffers schema language:

.. code-block:: proto

    syntax = "proto3";

    package countplugin1;

    service Counter {
        rpc Count(Count.Request) returns (Count.Response);
        rpc GetCount(GetCount.Request) returns (GetCount.Response);
    }

    message Count {
        message Request {
        }
        message Response {
        }
    }

    message GetCount {
        message Request {
        }
        message Response {
            int64 count = 1;
        }
    }

The ``service`` block defines which RPC functions are expected for a "counter"
plugin, which in this example are ``Count`` and ``GetCount``. Each of those
functions accepts arguments and returns values using Protocol Buffers
"message" types, where in this case the interface is relatively simple and
only includes a ``count`` result from ``GetCount``.

The ``example`` directory has a ``generate.sh`` file which will translate this
service definition into importable Python code that we use in our client and
server implementations, by running the Protocol Buffers compiler:

.. code-block:: bash

    python -m grpc_tools.protoc -I. \
        --python_out=. --grpc_python_out=. \
        countplugin1.proto

The above command generates two files: ``countplugin1_pb2.py`` and
``countplugin1_pb2_grpc.py``. These files contain generated Python classes
for both RPC clients ("stubs") and RPC servers ("servicers"), derived from
the service definition and message types in the ``.proto`` file.

Inside the Server
-----------------

In RPCPlugin terminology, the "server" is the plugin itself. This terminology
indicates that the plugin starts up a gRPC server ready for the calling
application (the "client") to connect to. Because of that, our server
implementation consists mainly of implementing the ``Counter`` gRPC service in
Python.

The source file ``server.py`` is the entry point for our count plugin server
written in Python. We'll just look at some snippets from that file here, but
please do refer to the whole file to see how it all fits together into a
working example.

.. code-block:: python

    import rpcplugin

    rpcplugin.serve(
        handshake=rpcplugin.Handshake(
            cookie_key="COUNT_PLUGIN_COOKIE",
            cookie_value="e8f9c7d7-20fd-55c7-83f9-bee91db2922b",
        ),
        proto_versions={
            1: CountPlugin1,
        },
    )

:py:func:`rpcplugin.serve` is the entry-point for plugin servers, and accepts
a number of arguments describing the intended plugin behavior. The above is
a minimal example using only two arguments:

* ``handshake`` defines an environment variable and its associated value which
  the client will set to allow this server to detect whether or not it is
  running as a plugin server. These values must agree exactly with the client
  and are normally defined as part of the plugin protocol definition of a
  particular application.

* ``proto_versions`` refers to the server implementation for each major version
  of the "counter" plugin protocol. As systems evolve it may eventually be
  necessary to introduce breaking changes via a new major protocol version, so
  this mapping allows for multiple versions to be implemented at once for
  a more graceful deprecation path.

There is only one major version (1) defined for the "count" protocol so far,
and its implementation is ``CountPlugin1`` which we will look at next.

.. code-block:: python

    import countplugin1_pb2
    import countplugin1_pb2_grpc

    class CountPlugin1(countplugin1_pb2_grpc.CounterServicer):
        def __init__(self, grpc_server):
            countplugin1_pb2_grpc.add_CounterServicer_to_server(
                self, grpc_server,
            )
            self.count = 0

        def Count(self, request, context):
            self.count += 1
            return countplugin1_pb2.Count.Response()

        def GetCount(self, request, context):
            return countplugin1_pb2.GetCount.Response(count=self.count)

``CountPlugin1`` is our class implementing the server side of the Counter
plugin service definition. We inherit from
``countplugin1_pb2_grpc.CounterServicer``, which is a class that was generated
by the protocol buffers compiler earlier.

The ``__init__`` method ensures that this class, when called, has the signature
expected for the callables in the ``proto_versions`` map in the ``serve`` call
above, which is:

.. code-block:: python

    callable(grpc_server)

Its responsibility then is to register ``CountPlugin1`` as the implementation
of ``CounterServicer`` for this server, which means that subsequent calls
to either ``Count`` or ``GetCount`` will be served by the methods of those
same names on our ``CountPlugin1`` instance.

The requirements of the ``Counter`` service are straightforward: each call
to ``Count`` increments the counter, and ``GetCount`` retrieves the current
counter value. We've implemented both of those behaviors here and ensured
that each implementation returns the appropriate Python type corresponding to
the expected response message type.

If you run ``python server.py`` directly you'll see it print an error message:

    Exception: calling program is not an rpcplugin host

That's because it's expecting to find the environment variable we declared
in ``handshake`` above, which would normally be set by the plugin client to
help detect when a plugin server is inadvertently used with the wrong calling
program, or run directly like this. To actually try out the ``server.py``
functionality we need a plugin *client* program, which we'll see in the
next section.

Inside the Client
-----------------

As noted above, the "client" in RPCPlugin is the host program that is
activating and calling into the plugins, which are the "servers". In our
``example`` directory the source file ``client.py`` contains a simplistic
client for the "Counter" plugin type, which by default launches the server
implementation we discussed in the previous section.

Again we'll just look at some snippets from the file; please refer to the
file itself to see how it all fits together.

.. code-block:: python

    import rpcplugin

    plugin = rpcplugin.start(
        args=('python', 'server.py'),
        handshake=rpcplugin.Handshake(
            cookie_key="COUNT_PLUGIN_COOKIE",
            cookie_value="e8f9c7d7-20fd-55c7-83f9-bee91db2922b",
        ),
        proto_versions={
            1: countplugin1_pb2_grpc.CounterStub,
        }
    )

:py:func:`rpcplugin.start` launches a child program (given by `args`) and
expects it to produce the rpcplugin handshake, returning a
:py:class:`rpcplugin.Plugin` object representing that child process.

Similarly to the server, we must provide a map of protocol version
implementations, this time in the form of a callable that takes a gRPC
channel and returns a client stub object. ``CounterStub`` is another class
generated by the protocol buffers compiler, this time providing a method
for each service function that forwards each call to the plugin server.

Once the plugin has started up, we can retrieve the client object for
the protocol version that the client and server negotiated:

.. code-block:: python

    proto_version, client = plugin.client()
    assert(proto_version == 1)  # only one version is supported

In an application supporting multiple protocol versions at once, we could
use the returned protocol version to know which service interface to expect,
but in our simple example there is only one version so we just assert that it
was selected.

.. code-block:: python

    client.Count(countplugin1_pb2.Count.Request())
    resp = client.GetCount(countplugin1_pb2.GetCount.Request())
    logging.info("counter value is now %d" % resp.count)

We can then call methods on the ``client`` object to call into the plugin.

Once we don't need the plugin anymore, we must shut it down by calling
:py:meth:`rpcplugin.Plugin.close`:

.. code-block:: python

    plugin.close()

Once ``close`` returns successfully, the child process for the plugin has
been terminated. The ``plugin`` and ``client`` objects are then no longer
usable.

Cross-language Calls
--------------------

Our ``client.py`` defaults to running the ``server.py`` in the same directory
as its plugin server, but if you pass it at least one argument then it will
use those arguments as the server command line.

There are no other language servers in the Python library repository, but if
you have a ``countplugin1`` server example in another language available to run
then you can pass it to ``client.py`` to see a cross-language call. For
example, if you have the Go_ server example in the default Go binary directory,
you could run the Go server in the Python client like this:

.. code-block:: bash

    python client.py ~/go/bin/count-plugin-server

Conversely, you can try the Python server with the Go client.

.. _RPCPlugin: https://www.rpcplugin.org/
.. _gRPC: https://www.grpc.io/
.. _`Protocol Buffers`: https://developers.google.com/protocol-buffers/
.. _Go: https://www.golang.org/
