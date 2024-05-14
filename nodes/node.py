import grpc
import leveldb
import time
import threading
from concurrent import futures
from grpc_health.v1 import health_pb2, health_pb2_grpc
from grpc_health.v1 import health
import kvstore_pb2
import kvstore_pb2_grpc
import logging
# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KeyValueStoreServicer(kvstore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, node_id, peers):
        self.db = leveldb.LevelDB(f'./db_{node_id}')
        self.node_id = node_id
        self.peers = peers
        self.replica_ids = [(node_id + i) % len(peers) for i in range(1, 3)]
        self.processed_requests = set()

    def replicate(self, key, value, source_node_id):
        for peer in self.replica_ids:
            if peer == source_node_id:
                continue  # Skip replication back to the source node
            retry_count = 0
            max_retries = 3
            while retry_count < max_retries:
                try:
                    with grpc.insecure_channel(self.peers[peer]) as channel:
                        stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)

                        stub.Put(kvstore_pb2.PutRequest(
                            key=key, value=value, source_node_id=self.node_id))
                        logger.debug(f"Replicated key: {key} to peer: {peer}")
                        break
                except grpc.RpcError as e:
                    retry_count += 1
                    logger.warning(
                        f"Failed to replicate key: {key} to peer: {peer}, retry {retry_count}/{max_retries}")
                    time.sleep(2 ** retry_count)

    def Put(self, request, context):
        request_id = (request.key, request.source_node_id)
        if request_id in self.processed_requests:
            logger.debug(f"Request {request_id} already processed")
            return kvstore_pb2.PutResponse(success=True)

        self.processed_requests.add(request_id)

        if request.source_node_id == self.node_id:
            logger.debug(f"Request {request_id} is a local request")
            return kvstore_pb2.PutResponse(success=True)

        logger.debug(
            f"Storing key: {request.key} with value: {request.value} in node {self.node_id}")
        self.db.Put(request.key.encode('utf-8'), request.value.encode('utf-8'))
        self.replicate(request.key, request.value, request.source_node_id)
        return kvstore_pb2.PutResponse(success=True)

    def Get(self, request, context):
        logger.debug(
            f"Get request received for key: {request.key}, replicated: {request.replicated}")
        if request.replicated:
            try:
                value = self.db.Get(
                    request.key.encode('utf-8')).decode('utf-8')
                logger.debug(f"Key: {request.key} found in primary node")
                return kvstore_pb2.GetResponse(value=value, found=True)
            except Exception:
                logger.debug(f"Key: {request.key} replicatd exption")
                return kvstore_pb2.GetResponse(found=False)

        else:
            try:
                value = self.db.Get(
                    request.key.encode('utf-8')).decode('utf-8')
                logger.debug(f"Key: {request.key} found in primary node")
                return kvstore_pb2.GetResponse(value=value, found=True)
            except Exception:
                logger.debug(
                    f"Key: {request.key} not found in primary node, looking in replicas")
                for peer in self.replica_ids:
                    try:
                        with grpc.insecure_channel(self.peers[peer]) as channel:
                            stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
                            response = stub.Get(kvstore_pb2.GetRequest(
                                key=request.key, source_node_id=self.node_id, replicated=True), timeout=1.0)
                            if response.found:
                                logger.debug(
                                    f"Key: {request.key} found in replica node {peer}")
                                return kvstore_pb2.GetResponse(value=response.value, found=True)
                    except grpc.RpcError:
                        logger.warning(
                            f"Failed to connect to replica node {peer}: {grpc.RpcError}")
                        continue
                logger.debug(
                    f"Key: {request.key} not found in any replica node")
                return kvstore_pb2.GetResponse(found=False)

    def Delete(self, request, context):
        try:
            self.db.Delete(request.key.encode('utf-8'))
            logger.debug(f"Key: {request.key} deleted from primary node")
            self.processed_requests = set()

            for peer in self.replica_ids:
                retry_count = 0
                max_retries = 2
                while retry_count < max_retries:
                    try:
                        with grpc.insecure_channel(self.peers[peer]) as channel:
                            stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
                            stub.Delete(kvstore_pb2.DeleteRequest(
                                key=request.key, source_node_id=self.node_id), timeout=1.0)
                            logger.debug(
                                f"Deleted key: {request.key} from replica node {peer}")
                            break
                    except grpc.RpcError as e:
                        retry_count += 1
                        logger.warning(
                            f"Failed to delete key: {request.key} from replica node {peer}, retry {retry_count}/{max_retries}")
                        time.sleep(2 ** retry_count)
                        if retry_count >= max_retries:
                            logger.error(
                                f"Exceeded max retries for deleting key: {request.key} from replica node {peer}")
                            break
            return kvstore_pb2.DeleteResponse(success=True)
        except KeyError:
            return kvstore_pb2.DeleteResponse(success=False)


def serve(node_id, peers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(node_id, peers), server)

    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set('grpc.health.v1.Health',
                        health_pb2.HealthCheckResponse.SERVING)

    server.add_insecure_port(peers[node_id])

    server.start()
    server.wait_for_termination()


def health_check(peers):
    time.sleep(10)  # Wait for 10 seconds to allow servers to start
    while True:
        for peer in peers:
            try:
                with grpc.insecure_channel(peer) as channel:
                    stub = health_pb2_grpc.HealthStub(channel)
                    response = stub.Check(health_pb2.HealthCheckRequest(
                        service='grpc.health.v1.Health'))
                    if response.status != health_pb2.HealthCheckResponse.SERVING:
                        logger.warning(f"Node {peer} is down")
            except Exception as e:
                logger.warning(f"Failed to connect to {peer}: {e}")

        time.sleep(5)


if __name__ == '__main__':
    import sys
    node_id = int(sys.argv[1])
    peers = ["kvstore-node1:50051",
             "kvstore-node2:50052", "kvstore-node3:50053"]
    threading.Thread(target=health_check, args=(peers,)).start()
    serve(node_id, peers)
