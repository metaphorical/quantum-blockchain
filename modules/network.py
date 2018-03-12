import socket, json, requests
# registering on the network, currently no channel to broadcast, so we can use ping to everyone in genesis nodes list
# TODO: discover and register on new peers by getting data about peers registered on network
# TODO: implement timeout for request and fallback... Probably hardcoded genesis node should be fallback and some (maybe serverless?) discovery mechanism should be created
# TODO: review ip fetching, must be less hacky way

def register_and_discover(node_addr, this_node):
    discover_payload = {'host': this_node}
    register_request = requests.post("{}/discover".format(node_addr), json=discover_payload)
    print(register_request.text)
    return register_request

def discover_network(genesis_node, live_nodes=[], port=5000):
    if not genesis_node:
        node_ip = socket.gethostbyname(socket.gethostname())
        this_node = "http://{}:{}".format(node_ip, port)
        new_nodes = []
        for qbc_node in live_nodes:

            hosts_from_node = json.loads(register_and_discover(qbc_node, this_node).text)

            new_nodes += [x for x in hosts_from_node if (x != this_node and x not in live_nodes)]

            print(json.dumps(new_nodes))

            if(len(new_nodes) > 0):
                live_nodes += new_nodes
                for new_node in new_nodes:
                    if node_ip not in new_node:
                        node_addr = new_node
                    else:
                        node_addr = new_node.replace(node_ip, "localhost")
                    print(node_addr)
                    json.loads(register_and_discover(node_addr, this_node).text)
            else:
                print("I guess this is second node on the network...")