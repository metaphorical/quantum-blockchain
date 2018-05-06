import json, socket, sys

system_config = json.load(open('./config/system_preferences.json'))

def get_current_ip():
    return socket.gethostbyname(socket.gethostname())

def get_port():
    return int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

def parse_localhost(new_node):
    """
        for testing purposes, for node to communicate inside same machine, 
        we need to parse all the IP addresses and replace current machine ones with localhost
    """
    current_node_ip = get_current_ip()
    if current_node_ip not in new_node:
        node_addr = new_node
    else:
        node_addr = new_node.replace(current_node_ip, "localhost")
    return node_addr

def is_genesis_node():
    # TODO: not by port but by full genesis nodes list lookup
    port = get_port()
    return port==5000