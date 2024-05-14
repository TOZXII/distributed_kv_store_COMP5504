from flask import Flask, request, render_template, redirect, url_for, flash
import grpc
import kvstore_pb2
import kvstore_pb2_grpc


app = Flask(__name__)
app.secret_key = 'supersecretkey'


nodes = ["kvstore-node1:50051", "kvstore-node2:50052", "kvstore-node3:50053"]


def get_stub(node):
    channel = grpc.insecure_channel(node)
    return kvstore_pb2_grpc.KeyValueStoreStub(channel)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/put', methods=['POST'])
def put():
    key = request.form['key']
    value = request.form['value']
    node = nodes[hash(key) % len(nodes)]
    stub = get_stub(node)
    try:
        response = stub.Put(kvstore_pb2.PutRequest(
            key=key, value=value, source_node_id=-1))
        if response.success:
            flash(f'Successfully stored key: {key}', 'success')
        else:
            flash(f'Failed to store key: {key}', 'error')
    except Exception as e:

        flash(f'Failed to store key: {key}', 'error')
    return redirect(url_for('index'))


@app.route('/get', methods=['POST'])
def get():
    key = request.form['key']
    node = nodes[hash(key) % len(nodes)]
    stub = get_stub(node)
    try:
        response = stub.Get(kvstore_pb2.GetRequest(key=key))
        if response.found:
            flash(f'Key: {key}, Value: {response.value}', 'success')
        else:
            flash(f'Key not found: {key}', 'error')
    except Exception as e:

        flash(f'Failed to retrieve key: {key}', 'error')
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    node = nodes[hash(key) % len(nodes)]
    stub = get_stub(node)
    try:
        response = stub.Delete(kvstore_pb2.DeleteRequest(key=key))
        if response.success:
            flash(f'Successfully deleted key: {key}', 'success')
        else:
            flash(f'Failed to delete key: {key}', 'error')
    except Exception as e:

        flash(f'Failed to delete key: {key}', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
