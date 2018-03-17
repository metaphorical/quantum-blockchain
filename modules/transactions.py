import requests, json, socket

from modules.network import parse_localhost

def broadcast_transaction(nodes, transaction, port):
    node_ip = socket.gethostbyname(socket.gethostname())
    this_node = parse_localhost("http://{}:{}".format(node_ip, port))
    for node in nodes:
        node = parse_localhost(node)
        if node != this_node:
            r = requests.put("{}/inject".format(node), json={"data":transaction})
            print(r.text)