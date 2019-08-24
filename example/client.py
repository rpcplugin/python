import logging
import os
import os.path
import sys
import time


import rpcplugin
import countplugin1_pb2
import countplugin1_pb2_grpc


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.info("python count plugin server starting up")

    args = sys.argv[1:]
    if len(args) == 0:
        args = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), 'server.py'),
        ]

    logging.info("launching plugin %r" % args)
    plugin = rpcplugin.start(
        args=args,
        handshake=rpcplugin.Handshake(
            cookie_key="COUNT_PLUGIN_COOKIE",
            cookie_value="e8f9c7d7-20fd-55c7-83f9-bee91db2922b",
        ),
        proto_versions={
            1: lambda chan: countplugin1_pb2_grpc.CounterStub(chan),
        }
    )

    proto_version, client = plugin.client()
    assert(proto_version == 1)  # only one version is supported

    try:
        logging.info(
            "will increment the counter every two seconds until interrupted",
        )
        while True:
            logging.info("incrementing the counter")
            client.Count(countplugin1_pb2.Count.Request())
            resp = client.GetCount(countplugin1_pb2.GetCount.Request())
            logging.info("counter value is now %d" % resp.count)
            time.sleep(2)

    except KeyboardInterrupt:
        pass


main()
