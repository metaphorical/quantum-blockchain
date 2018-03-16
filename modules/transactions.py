import requests, json, socket

def broadcast_transaction(nodes, transaction, port):
    node_ip = socket.gethostbyname(socket.gethostname())
    this_node = "http://{}:{}".format(node_ip, port)
    for node in nodes:
        if node != this_node:
            requests.put("{}/inject".format(node), data=json.dumps(transaction))