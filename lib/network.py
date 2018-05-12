import os, json, requests, pickle

from lib.qbc_utils import parse_localhost, is_genesis_node, get_port, get_current_ip, get_hostname
# registering on the network, currently no channel to broadcast, so we can use ping to everyone in genesis nodes list
# TODO: Convert this blob to Class and load and save in constructor.
# TODO: implement timeout for request and fallback... Probably hardcoded genesis node should be fallback and some (maybe serverless?) discovery mechanism should be created

def load_nodes():
    with open(os.path.join(os.getcwd(),'storage', 'nodes.json'), 'rb') as node_file:
            return json.load(node_file)

def save_nodes(nodes):  
    with open(os.path.join(os.getcwd(),'storage', 'nodes.json'), 'wb') as fp:
            json.dumps(nodes, fp)  

def get_this_node():
    node_ip = get_current_ip()
    return get_hostname(node_ip, get_port())

def register_and_discover(node_addr, this_node):
    discover_payload = {'host': this_node}
    register_request = requests.post("{}/discover".format(node_addr), json=discover_payload)
    print("register and discover - {}".format(register_request.text))
    return register_request

def read_chain(node_addr):
    """
        TODO: this might probably grow to be first secure transfer point, so when working on 
        node to node auth, include it here
    """
    chain_request = requests.get("{}/chain".format(node_addr))
    return chain_request.text

def broadcast_quant(nodes, quant):
    """
        Broadcast any quant to all nodes in provided list
        TODO: secure this process
    """
    this_node = parse_localhost(get_this_node())
    for qbc_node in nodes:
        node_addr = parse_localhost(qbc_node)
        if node_addr != this_node:
            print node_addr
            quant_payload = {'quant': pickle.dumps(quant)}
            request = requests.post("{}/add-block".format(node_addr), json=quant_payload)
            print("Broadcasted new block to {} - {}".format(node_addr, request.text))



def discover_network(live_nodes=[]):
    """
        Network discovery is done in two stages:
        1 - ping genesys node (aka tracker) to register and get it's full list of nodes
        2 - register on all of the nodes
        TODO: implement cross check and re register of nodes.
    """
    registered_nodes = load_nodes()
    new_nodes = []
    max_length = 0
    max_length_node = ""
    if not is_genesis_node():
        this_node = get_this_node()
        for qbc_node in registered_nodes:
            node_addr = parse_localhost(qbc_node)
            # Reading chain stats and checking chain length, if chain length is higher we set it in max_length var
            node_chain_length = json.loads(register_and_discover(node_addr, this_node).text)["stats"]["length"]
            if(node_chain_length > max_length):
                max_length = node_chain_length
                max_length_node = node_addr
            # Getting live nodes and figuring out new ones
            hosts_from_node = json.loads(register_and_discover(node_addr, this_node).text)["live_nodes"]

            new_nodes += [x for x in hosts_from_node if (x != this_node and x not in registered_nodes)]

            print("new nodes - {}".format(json.dumps(new_nodes)))

            registered_nodes = registered_nodes + new_nodes
            if(len(new_nodes) > 0):
                print("registered nodes - {}".format(json.dumps(registered_nodes)))
                for new_node in new_nodes:
                    new_node_addr = parse_localhost(new_node)
                    register_and_discover(new_node_addr, this_node)
            else:
                print("I guess this is second node on the network...")
    return {
        "registered_nodes": registered_nodes,
        "longest_chain_length": max_length,
        "longest_chain_node": max_length_node
    }