import json, socket

def json_serialize_chain(qbc):
    """
        Getting json serialized QBC
    """
    return json.dumps([{
				"index": str(quant.index),
				"timestamp": str(quant.timestamp),
				"data": str(quant.data),
				"hash": quant.hash,
				"proof": str(quant.proof)
				} for quant in qbc])

def parse_localhost(new_node):
    """
        for testing purposes, for node to communicate inside same machine, 
        we need to parse all the IP addresses and replace current machine ones with localhost
    """
    current_node_ip = socket.gethostbyname(socket.gethostname())
    if current_node_ip not in new_node:
        node_addr = new_node
    else:
        node_addr = new_node.replace(current_node_ip, "localhost")
    return node_addr