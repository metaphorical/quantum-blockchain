import requests, json

from modules.qbc_utils import parse_localhost, get_current_ip, get_port, get_hostname

def broadcast_transaction(nodes, transaction, port):
    node_ip = get_current_ip()
    port = get_port()
    this_node = parse_localhost(get_hostname(node_ip, port))
    for node in nodes:
        node = parse_localhost(node)
        if node != this_node:
            r = requests.put("{}/inject".format(node), json={"data":transaction})
            print(r.text)