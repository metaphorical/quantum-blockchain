import os, json, requests, pickle

from lib.qbc_utils import QbcUtils

QBCU = QbcUtils()

# TODO: implement timeout for request and fallback... Probably hardcoded genesis node should be fallback and some (maybe serverless?) discovery mechanism should be created
# TODO: All the saves and loads should be improved by adding in memory storage for performance and encryption for security

class Network:
    def load_nodes(self):
        with open(os.path.join(os.getcwd(),'storage', 'nodes.json'), 'rb') as node_file:
            nodes_json = json.load(node_file)
            print("NODES {}".format(nodes_json))
            return nodes_json

    def save_nodes(self, nodes):
        # import pdb; pdb.set_trace()
        with open(os.path.join(os.getcwd(),'storage', 'nodes.json'), 'wb') as fp:
            json.dump(nodes, fp)

    def get_this_node(self):
        node_ip = QBCU.get_current_ip()
        return QBCU.get_hostname(node_ip, QBCU.get_port())

    def register_and_discover(self, node_addr, this_node):
        discover_payload = {'host': this_node}
        try:
            register_request = requests.post("{}/discover".format(node_addr), json=discover_payload)
        except ValueError:
            print("register and discover ERROR - {}".format(ValueError))
            register_request = False
        print("register and discover - {}".format(register_request.text))
        return register_request

    def read_chain(self, node_addr):
        """
            TODO: this might probably grow to be first secure transfer point, so when working on
            node to node auth, include it here
        """
        chain_request = requests.get("{}/chain".format(node_addr))
        return chain_request.text

    def broadcast_quant(self, nodes, quant):
        """
            Broadcast any quant to all nodes in provided list
            TODO: secure this process
        """
        this_node = QBCU.parse_localhost(self.get_this_node())
        for qbc_node in nodes:
            node_addr = QBCU.parse_localhost(qbc_node)
            if node_addr != this_node:
                print node_addr
                quant_payload = {'quant': pickle.dumps(quant)}
                request = requests.post("{}/add-block".format(node_addr), json=quant_payload)
                print("Broadcasted new block to {} - {}".format(node_addr, request.text))

    def discover_network(self, live_nodes=[]):
        """
            Network discovery is done in two stages:
            1 - ping genesys node (aka tracker) to register and get it's full list of nodes
            2 - register on all of the nodes
            TODO: implement cross check and re register of nodes.
        """
        registered_nodes = self.load_nodes()
        new_nodes = []
        max_length = 0
        max_length_node = ""
        if not QBCU.is_genesis_node():
            this_node = self.get_this_node()
            print("THIS NODE {}".format(this_node))
            for qbc_node in registered_nodes:
                # When node boots up again it will have self on the node list
                # We need to make sure that it does not try to call self in discovery process
                if qbc_node != self.get_this_node():
                    node_addr = QBCU.parse_localhost(qbc_node)
                    # Reading chain stats and checking chain length, if chain length is higher we set it in max_length var
                    discover_node = self.register_and_discover(node_addr, this_node)
                    
                    # Before implementing retries, we assume that there is no node
                    if discover_node:
                        node_chain_length = json.loads(discover_node.text)["stats"]["length"]
                    else:
                        node_chain_length = 0

                    if(node_chain_length > max_length):
                        max_length = node_chain_length
                        max_length_node = node_addr
                    # Getting live nodes and figuring out new ones (no nodes if node not live)
                    if discover_node:
                        hosts_from_node = json.loads(discover_node.text)["live_nodes"]  
                    else: 
                        hosts_from_node = []

                    new_nodes += [x for x in hosts_from_node if (x != this_node and x not in registered_nodes)]

                    print("new nodes - {}".format(json.dumps(new_nodes)))

                    registered_nodes = registered_nodes + new_nodes
                    self.save_nodes(registered_nodes)
                    if(len(new_nodes) > 0):
                        print("registered nodes - {}".format(json.dumps(registered_nodes)))
                        for new_node in new_nodes:
                            new_node_addr = QBCU.parse_localhost(new_node)
                            self.register_and_discover(new_node_addr, this_node)
                    else:
                        print("I guess this is second node on the network...")
        return {
            "registered_nodes": registered_nodes,
            "longest_chain_length": max_length,
            "longest_chain_node": max_length_node
        }