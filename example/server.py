import logging
import sys

import rpcplugin
import countplugin1_pb2
import countplugin1_pb2_grpc


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.info("python count plugin server starting up")

    rpcplugin.serve(
        handshake=rpcplugin.Handshake(
            cookie_key="COUNT_PLUGIN_COOKIE",
            cookie_value="e8f9c7d7-20fd-55c7-83f9-bee91db2922b",
        ),
        proto_versions={
            1: CountPlugin1,
        },
        signal_handlers=False,  # temporarily while debugging
    )


class CountPlugin1(countplugin1_pb2_grpc.CounterServicer):
    def __init__(self, grpc_server):
        countplugin1_pb2_grpc.add_CounterServicer_to_server(self, grpc_server)
        self.count = 0

    def Count(self, request, context):
        self.count += 1
        return countplugin1_pb2.Count.Response()

    def GetCount(self, request, context):
        return countplugin1_pb2.Count.Response(count=self.count)


main()
