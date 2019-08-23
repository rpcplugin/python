.. rpcplugin documentation master file, created by
   sphinx-quickstart on Fri Aug 23 07:33:05 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

RPCPlugin for Python
====================

RPCPlugin_ is a cross-language application plugin mechanism, with plugins
running as child processes and communicating with their host using gRPC_ and
protocol buffers.

This is the documentation for the Python implementation of RPCPlugin, which
allows writing both plugin clients (the host application) and plugin servers
(the plugins themselves) in Python, while remaining compatible with the
RPCPlugin implementations for other languages.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro

.. _RPCPlugin: https://www.rpcplugin.org/
.. _gRPC: https://www.grpc.io/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
